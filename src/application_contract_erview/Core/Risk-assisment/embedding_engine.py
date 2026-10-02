# Core/Risk-assisment/embedding_engine.py
import sys
from pathlib import Path
from typing import Union, List
from sentence_transformers import SentenceTransformer

CURRENT_DIR = Path(__file__).resolve().parent
APP_DIR = CURRENT_DIR.parents[1]
sys.path.insert(0, str(APP_DIR))

from helpers.config import AppConfig

class EmbeddingEngine:
    def __init__(self):
        """
        Initializes the shared dense embedding transformer framework using AppConfig constants.
        """
        print(f"Initializing Shared Embedding Engine model: {AppConfig.EMBEDDING_MODEL_NAME}...")
        self.model = SentenceTransformer(AppConfig.EMBEDDING_MODEL_NAME)

    def get_embeddings(self, text_input: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Transforms string inputs into 768-dimensional mathematical array vectors.
        """
        if isinstance(text_input, str):
            return self.model.encode(text_input).tolist()
        elif isinstance(text_input, list):
            return [self.model.encode(text).tolist() for text in text_input]
        else:
            raise TypeError("Embedding input layout must be a string or a sequence list of strings.")

# Globally shared instantiation node to preserve GPU VRAM memory space
shared_embedding_engine = EmbeddingEngine()
