import sys
import logging
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent
SOURCE_ROOT = CURRENT_DIR.parents[1] / "src"
CONFIG_FILE = next(SOURCE_ROOT.glob("*/helpers/config.py"))
APP_PACKAGE_DIR = CONFIG_FILE.parents[1]
sys.path.append(str(APP_PACKAGE_DIR))

from helpers.config import AppConfig

def setup_risk_collection():
    """Connect to Qdrant and create the risk collection if it does not exist."""
    logger.info("Connecting to Qdrant at %s", AppConfig.QDRANT_URL)
    client = QdrantClient(url=AppConfig.QDRANT_URL)

    if client.collection_exists(AppConfig.RISK_COLLECTION_NAME):
        logger.info(
            "Collection '%s' already exists; preserving its stored vectors.",
            AppConfig.RISK_COLLECTION_NAME,
        )
        return

    logger.info(
        "Creating collection '%s' with %s-dimensional cosine vectors.",
        AppConfig.RISK_COLLECTION_NAME,
        AppConfig.EMBEDDING_DIMENSION,
    )
    client.create_collection(
        collection_name=AppConfig.RISK_COLLECTION_NAME,
        vectors_config=VectorParams(
            size=AppConfig.EMBEDDING_DIMENSION,
            distance=Distance.COSINE,
        ),
    )
    logger.info("Collection '%s' is ready.", AppConfig.RISK_COLLECTION_NAME)

if __name__ == "__main__":
    setup_risk_collection()
