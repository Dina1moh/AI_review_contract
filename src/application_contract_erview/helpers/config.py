import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve the repository root directory.
BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=BASE_DIR / ".env")

class AppConfig:
    # Qdrant Vector DB Settings
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    RISK_COLLECTION_NAME = os.getenv("RISK_COLLECTION_NAME", "risk_rules")
    
    # Dense Embedding Settings for Text Evaluation
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-mpnet-base-v2")
    EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 768))
    
    # Legal Textbook Chunking Parameters
    RISK_BOOK_PATH = os.getenv("RISK_BOOK_PATH")
    EDURISK_GUIDE_PATH = os.getenv("EDURISK_GUIDE_PATH")
    RISK_CHUNK_SIZE = int(os.getenv("RISK_CHUNK_SIZE", 700))
    RISK_CHUNK_OVERLAP = int(os.getenv("RISK_CHUNK_OVERLAP", 120))
    
    # Local LLM Server Parameters
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://ngrok-free.dev")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "qwen3.5-4b")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.0))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 1024))
    LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", 60.0))
