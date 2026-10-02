# Technical Documentation: Offline Risk Knowledge Base Preparation

## 1. Architectural Design Overview
The Risk Assessment module (Stage 3) of the contract review pipeline operates on a decoupled architecture. Before processing live user contracts online, the system establishes a local Knowledge Base offline. This structure converts legal textbooks into dense vector spaces to enable semantic retrieval during inference time.

The configuration ecosystem is centralized inside a shared configuration module (`config.py`) which reads system environment parameters directly from a core `.env` file. This shared paradigm guarantees that both offline ingestion and online retrieval pipelines point to identical embedding models, dimension spaces, and database collections, minimizing configuration divergence.

---

## 2. Directory and File Map

```text
APPLICATION_CONTRACT_REVIEW/
│
├── .env                                       # System environment variable configurations
│
├── data/
│   └── drafting-and-negotiating..._compress.pdf # Compressed source commercial contract textbook
│
├── offline/
│   └── Risk-assisment/
│       ├── vector_db_setup.py                 # Structural database initializer module
│       ├── ingest_risk_playbook.py            # LangChain-powered document ingestion engine
│       └── run_risk_offline.py                # Main offline orchestrator runner script
│
└── src/
    └── application_contract_review/
        └── helpers/
            └── config.py                      # Core shared configuration class configuration
```

---

## 3. Configuration Specification

### A. Environment Configuration (`.env`)
Defines the dynamic variables that dictate the vector database collection, baseline mathematical dimensions, local storage paths, and the exact sliding-window parameters for chunking operations.

### B. AppConfig Class (`config.py`)
Parses the runtime environment properties into a unified Python singleton object using `pathlib` and `dotenv`. 
*   **Properties Managed:**
    *   `QDRANT_URL`: Network location of the local vector database instance.
    *   `RISK_COLLECTION_NAME`: Targeted Qdrant storage namespace for playbook regulations.
    *   `EMBEDDING_MODEL_NAME`: Local Hugging Face transformer model identifier.
    *   `EMBEDDING_DIMENSION`: Integer representing vector widths (768 for MPNet).
    *   `RISK_BOOK_PATH`: Absolute path to the source compressed legal PDF.
    *   `RISK_CHUNK_SIZE` & `RISK_CHUNK_OVERLAP`: Text segmentation thresholds.

---

## 4. Module Functionality & Code Analysis

### A. Vector Database Initializer (`vector_db_setup.py`)
Responsible for ensuring a pristine database architecture prior to indexing data blocks.

*   **Function:** `setup_risk_collection()`
    *   **Input parameters:** None (Queries `AppConfig` directly).
    *   **Internal Operations:** Establishes an HTTP connection to the Qdrant database instance via `QdrantClient`. It triggers an isolated structural recreation directive (`client.recreate_collection`) forcing an empty collection mapped specifically to the designated vector dimension size and configured to measure spatial alignment using `Distance.COSINE`.
    *   **Output / Side Effect:** Purges any stale data and provisions an active, empty table structure ready to parse payload packets.

### B. Playbook Processing & Ingestion Engine (`ingest_risk_playbook.py`)
The functional core utilizing LangChain abstraction libraries to digest legal syntax into indexable items.

*   **Function:** `ingest_playbook()`
    *   **Input parameters:** None (Queries `AppConfig` directly).
    *   **Internal Operations:**
        1.  Verifies the local physical existence of the compressed textbook using `os.path.exists`.
        2.  Executes full-text document parsing by instantiating LangChain's **`PyPDFLoader`**, transforming the static PDF layout into unified sequential document nodes.
        3.  Initializes text slicing by calling LangChain's **`RecursiveCharacterTextSplitter`**, passing the character length threshold and the overlapping bounds to keep related cross-page sentences intact.
        4.  Loads the localized `SentenceTransformer` text encoder to compute the 768-dimensional float arrays.
        5.  Constructs database point structural payloads (`PointStruct`), packing the numerical dense vector alongside a metadata map tracking the specific slice contents, page index number, and file reference origin.
        6.  Performs database upserts in managed block streams (Batch Size = 50) to prevent communication time-outs or memory starvation.
    *   **Output / Side Effect:** Embeds and indexes legal knowledge segments directly inside Qdrant storage.

### C. Pipeline Orchestrator (`run_risk_offline.py`)
Acts as the central execution runner to synchronize the execution nodes in proper structural order.

*   **Function:** `main()`
    *   **Execution Order:** Invokes `setup_risk_collection()` first to ensure structural readiness, then directly passes execution to `ingest_playbook()`. Wraps the execution nodes within a granular try-except block to gracefully catch, log, and terminate processing upon encountering file IO or database networking anomalies.

---

## 5. System Execution Manifest
To completely build the offline knowledge database architecture, the pipeline orchestrator can be executed within a shell or PowerShell environment using the following absolute routing command:

```powershell
python D:\APPLICATION_CONTRACT_REVIEW\offline\Risk-assisment\run_risk_offline.py
```
