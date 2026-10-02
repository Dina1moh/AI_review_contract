FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1 \
	PYTHONPATH=/app/src \
	RISK_BOOK_PATH=/app/data/risk_playbook.pdf \
	EDURISK_GUIDE_PATH=/app/data/edurisk_guide.pdf

RUN apt-get update \
	&& apt-get install -y --no-install-recommends libgomp1 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
	&& python -m pip install --index-url https://download.pytorch.org/whl/cu126 torch \
	&& python -m pip install -r requirements.txt

COPY src/application_contract_erview/ ./src/application_contract_erview/
COPY offline/Risk-assisment/ ./offline/Risk-assisment/
COPY data/drafting-and-negotiating-commercial-contracts-5nbsped-1526517248-9781526517241_compress.pdf ./data/risk_playbook.pdf
COPY data/united_educators_checklist_guide_for_reviewing_contracts.pdf ./data/edurisk_guide.pdf

CMD ["python", "offline/Risk-assisment/run_risk_offline.py"]
