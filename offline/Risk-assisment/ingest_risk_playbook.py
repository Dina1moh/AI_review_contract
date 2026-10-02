import sys
import os
import logging
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import torch

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent
SOURCE_ROOT = CURRENT_DIR.parents[1] / "src"
CONFIG_FILE = next(SOURCE_ROOT.glob("*/helpers/config.py"))
APP_PACKAGE_DIR = CONFIG_FILE.parents[1]
sys.path.append(str(APP_PACKAGE_DIR))

from helpers.config import AppConfig

def ingest_playbook():
    """
    Loads the commercial textbook via LangChain, executes text splitting, and updates the vector database.
    """
    pdf_path = AppConfig.RISK_BOOK_PATH
    
    # Verify the local existence of the contract textbook file
    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Target reference playbook PDF not found at: {pdf_path}")
        
    logger.info("Loading reference PDF: %s", os.path.basename(pdf_path))
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    logger.info(
        "Splitting text with chunk_size=%s and chunk_overlap=%s.",
        AppConfig.RISK_CHUNK_SIZE,
        AppConfig.RISK_CHUNK_OVERLAP,
    )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=AppConfig.RISK_CHUNK_SIZE,       
        chunk_overlap=AppConfig.RISK_CHUNK_OVERLAP,    
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(pages)
    logger.info("Generated %s text chunks.", len(chunks))
    
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable. Run the container with --gpus all and a CUDA-enabled PyTorch image.")

    logger.info("Loading embedding model %s on CUDA.", AppConfig.EMBEDDING_MODEL_NAME)
    embedding_model = SentenceTransformer(AppConfig.EMBEDDING_MODEL_NAME, device="cuda")
    client = QdrantClient(AppConfig.QDRANT_URL)
    
    logger.info("Embedding and uploading to collection '%s'.", AppConfig.RISK_COLLECTION_NAME)
    batch_size = 50
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        vectors = embedding_model.encode(
            [doc.page_content for doc in batch],
            batch_size=batch_size,
            show_progress_bar=False,
        )
        points = []
        for offset, (doc, vector) in enumerate(zip(batch, vectors)):
            payload = {
                "text": doc.page_content,
                "source_page": doc.metadata.get("page", 0) + 1,
                "source_file": os.path.basename(pdf_path),
            }
            points.append(
                PointStruct(
                    id=start + offset,
                    vector=vector.tolist(),
                    payload=payload,
                )
            )

        client.upsert(
            collection_name=AppConfig.RISK_COLLECTION_NAME,
            points=points,
        )
        logger.info("Processed %s/%s chunks.", min(start + len(batch), len(chunks)), len(chunks))
        
    logger.info("Ingestion completed for collection '%s'.", AppConfig.RISK_COLLECTION_NAME)

if __name__ == "__main__":
    ingest_playbook()
