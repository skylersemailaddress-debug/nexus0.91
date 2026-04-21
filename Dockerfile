FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip &&     if [ -f requirements.txt ]; then pip install -r requirements.txt; fi &&     if [ -f pyproject.toml ]; then pip install -e .; fi

CMD ["python", "scripts/run_enterprise_gate.py"]
