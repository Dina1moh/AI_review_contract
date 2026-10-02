import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))

# Import the new supplemental ingestion module only
from ingest_edurisk_playbook import ingest_edurisk_supplemental_guide

def main():
    # Utilizing localized CPU runtime configuration to process supplemental documents safely
    logger.info("Starting local supplemental knowledge base ingestion on CPU framework.")
    try:
        # Step 3: Append the supplemental EduRisk guidelines into the same persistent collection
        ingest_edurisk_supplemental_guide()
        
        logger.info("Offline risk assessment pipeline completed successfully. Data appended to Qdrant store.")
    except Exception:
        logger.exception("Offline risk assessment pipeline failed during local runtime execution.")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
