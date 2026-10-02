# Core/Risk-assisment/contract_preprocessor.py
import sys
from pathlib import Path
from typing import List, Dict, Any
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR.parents[2]))

from application_contract_review.helpers.config import AppConfig

def segment_contract_semantically(contract_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Applies zero-overlap character text splitting driven by sentence embeddings 
    to guarantee clean independent clause segment boundaries.
    """
    # Initialize LangChain semantic pipeline embedding matching
    embeddings = HuggingFaceEmbeddings(model_name=AppConfig.EMBEDDING_MODEL_NAME)
    
    # Instantiate text chunker configured to split when content transitions to a new legal context
    text_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")
    segmented_clauses = []
    
    for page in contract_pages:
        # Separate the targeted page block text
        docs = text_splitter.create_documents([page["text"]])
        
        for doc in docs:
            cleaned_text = doc.page_content.strip()
            # Suppress short debris, headers, or lines under 40 characters
            if len(cleaned_text) >= 40:
                segmented_clauses.append({
                    "text": cleaned_text,
                    "source_page": page["page_number"],
                    "source_file": page["source_file"]
                })
                
    return segmented_clauses
