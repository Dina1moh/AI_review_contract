import json
import logging
import sys
from pathlib import Path
from typing import Any

import httpx
from pydantic import ValidationError
from qdrant_client import QdrantClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

CURRENT_DIR = Path(__file__).resolve().parent
APP_DIR = next(
    (
        parent
        for parent in CURRENT_DIR.parents
        if (parent / "helpers" / "config.py").is_file()
    ),
    None,
)
if APP_DIR is None:
    raise ImportError("Could not locate the application directory containing helpers/config.py.")

sys.path.insert(0, str(APP_DIR))
sys.path.insert(0, str(CURRENT_DIR))

from helpers.config import AppConfig
from prompts.risk_prompt import get_risk_audit_prompt
from schemas.risk_schema import RiskAssessmentResponse
from embedding_engine import shared_embedding_engine

logger = logging.getLogger(__name__)
qdrant_client = QdrantClient(AppConfig.QDRANT_URL)


def retrieve_risk_playbook_contexts(query_text: str, limit: int = 5) -> str:
    """Retrieve and log the highest-scoring textbook passages for an audit query."""
    vector = shared_embedding_engine.get_embeddings(query_text)
    search_results = qdrant_client.query_points(
        collection_name=AppConfig.RISK_COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True,
    ).points
    logger.info(
        "Qdrant returned %d candidates from collection %r.",
        len(search_results),
        AppConfig.RISK_COLLECTION_NAME,
    )

    contexts: list[str] = []
    for rank, hit in enumerate(search_results, start=1):
        payload = hit.payload or {}
        text = payload.get("text")
        source_page = payload.get("source_page", "Unknown")
        source_file = payload.get("source_file", "Unknown")

        if not isinstance(text, str) or not text.strip():
            logger.warning(
                "Qdrant match rank=%d score=%r has no usable text payload "
                "(source_file=%r, source_page=%r).",
                rank,
                hit.score,
                source_file,
                source_page,
            )
            continue

        logger.info(
            "Qdrant cosine match rank=%d score=%r source_file=%r "
            "source_page=%r text_chars=%d",
            rank,
            hit.score,
            source_file,
            source_page,
            len(text),
        )
        logger.info("Qdrant raw textbook passage rank=%d:\n%s", rank, text)

        contexts.append(
            f"[Retrieved passage {rank}; source={source_file}; "
            f"page={source_page}; qdrant_cosine_score={hit.score!r}]\n{text}"
        )

    if not contexts:
        logger.warning(
            "Qdrant returned no usable textbook passages for collection %r.",
            AppConfig.RISK_COLLECTION_NAME,
        )
        return "No usable textbook passages were retrieved."

    return "\n\n".join(contexts)


def _unavailable_result(recommendation: str) -> dict[str, Any]:
    return {
        "assessment_status": "insufficient_evidence",
        "has_violation": False,
        "failed_checklist_question": "",
        "not_assessed_questions": ["Clause audit (LLM response unavailable or invalid)"],
        "clause_contradiction": "",
        "correct_rule_from_book": "",
        "risk_tier": "Unknown",
        "recommendation": recommendation,
    }


def _extract_json_content(response_json: dict[str, Any]) -> str:
    choices = response_json.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("LLM response did not contain any choices.")

    choice = choices[0]
    if not isinstance(choice, dict):
        raise ValueError("LLM response choice was not an object.")

    message = choice.get("message")
    if not isinstance(message, dict):
        raise ValueError("LLM response choice did not contain a message object.")

    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("LLM response message did not contain text content.")

    content = content.strip()
    if content.startswith("```") and content.endswith("```"):
        content = content[3:-3].strip()
        if content.startswith("json"):
            content = content[4:].strip()
    return content


def execute_risk_inference(clause_text: str, category_name: str) -> dict[str, Any]:
    """Retrieve textbook evidence, generate an audit, and validate the JSON response."""
    search_query = f"Contract category: {category_name}\nClause text: {clause_text}"
    context_str = retrieve_risk_playbook_contexts(search_query)
    prompt = get_risk_audit_prompt(context_str, category_name, clause_text)
    logger.info(
        "Compiled risk prompt for category=%r with retrieved_context_chars=%d "
        "and prompt_chars=%d.",
        category_name,
        len(context_str),
        len(prompt),
    )

    payload = {
        "model": AppConfig.LLM_MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": AppConfig.LLM_TEMPERATURE,
        "max_tokens": AppConfig.LLM_MAX_TOKENS,
        "response_format": {"type": "json_object"},
    }
    endpoint_url = f"{AppConfig.LLM_BASE_URL.rstrip('/')}/chat/completions"

    try:
        with httpx.Client(
            timeout=AppConfig.LLM_TIMEOUT_SECONDS,
            follow_redirects=True,
        ) as client:
            response = client.post(endpoint_url, json=payload)
            response.raise_for_status()
            response_json = response.json()
    except httpx.HTTPError:
        logger.exception("LLM request failed.")
        return _unavailable_result(
            "The LLM request failed. Check the configured OpenAI-compatible endpoint "
            "and retry; otherwise perform a manual review."
        )
    except json.JSONDecodeError:
        logger.exception("LLM endpoint returned a non-JSON response envelope.")
        return _unavailable_result(
            "The LLM endpoint returned an invalid response. Check the configured "
            "OpenAI-compatible endpoint and retry; otherwise perform a manual review."
        )

    try:
        if not isinstance(response_json, dict):
            raise ValueError("LLM response envelope was not a JSON object.")
        raw_content = _extract_json_content(response_json)
        parsed_response = json.loads(raw_content)
        validated_response = RiskAssessmentResponse.model_validate(parsed_response)
        if validated_response.risk_tier not in {"None", "Low", "Medium", "High", "Unknown"}:
            raise ValueError("LLM response contained an unsupported risk tier.")
        if validated_response.assessment_status == "violation" and not validated_response.has_violation:
            raise ValueError("A violation assessment must set has_violation to true.")
        if (
            validated_response.assessment_status in {"no_violation", "not_applicable"}
            and validated_response.has_violation
        ):
            raise ValueError("A non-violation assessment cannot set has_violation to true.")
    except (ValueError, KeyError, IndexError, TypeError, ValidationError):
        logger.exception("LLM returned content that failed JSON/schema validation.")
        return _unavailable_result(
            "The LLM response did not match the required risk-assessment JSON schema. "
            "Retry or perform a manual review."
        )

    return validated_response.model_dump()
