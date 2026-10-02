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

# Dynamic package discovery tailored to avoid naming issues
CURRENT_DIR = Path(__file__).resolve().parent
SOURCE_ROOT = CURRENT_DIR.parents[1] / "src"
CONFIG_FILE = next(SOURCE_ROOT.glob("*/helpers/config.py"))
APP_PACKAGE_DIR = CONFIG_FILE.parents[1]
sys.path.append(str(APP_PACKAGE_DIR))

from helpers.config import AppConfig

def ingest_edurisk_supplemental_guide():
    """
    Loads the supplemental EduRisk PDF, chunks via LangChain, and appends vectors to Qdrant.
    """
    edurisk_pdf_path = "D:/APPLICATION_CONTRACT_REVIEW/data/united_educators_checklist_guide_for_reviewing_contracts.pdf"
    
    if not os.path.exists(edurisk_pdf_path):
        raise FileNotFoundError(f"Target EduRisk PDF playbook not found at: {edurisk_pdf_path}")
        
    logger.info("Loading EduRisk supplemental playbook: %s", os.path.basename(edurisk_pdf_path))
    loader = PyPDFLoader(edurisk_pdf_path)
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
    logger.info("Generated %s supplemental risk text blocks.", len(chunks))

    logger.info("Loading embedding model %s on CPU.", AppConfig.EMBEDDING_MODEL_NAME)
    embedding_model = SentenceTransformer(AppConfig.EMBEDDING_MODEL_NAME, device="cpu")
    client = QdrantClient(AppConfig.QDRANT_URL)
    
    EDURISK_COLLECTION = "edurisk_rules"
    logger.info("Embedding and appending to collection '%s'.", EDURISK_COLLECTION)
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
                "source_file": os.path.basename(edurisk_pdf_path),
            }
            points.append(
                PointStruct(
                    id=start + offset,
                    vector=vector.tolist(),
                    payload=payload,
                )
            )

        client.upsert(
            collection_name=EDURISK_COLLECTION,
            points=points,
        )
        logger.info("Processed %s/%s supplemental blocks.", min(start + len(batch), len(chunks)), len(chunks))
        
    logger.info("Supplemental ingestion completed for collection '%s'.", EDURISK_COLLECTION)

if __name__ == "__main__":
    ingest_edurisk_supplemental_guide()
