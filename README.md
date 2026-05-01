Neosemantix — Quick Start
=========================

Overview
--------
Small pipeline that reads a sample input, performs Entity extraction using spaCy, and generates a summary via the configured LLM summarization service.

Repository
----------
Source code and diagrams are available at: https://github.com/avp1510/neosemantix-summarizer

System design (interactive): https://whimsical.com/system-design2525/system-design-9x3CG2LipJyeiUvSh8YNYp

Project layout (key files)
- `run.py` — entrypoint that wires components and prints results.
- `app/engine/api.py` — loads `GROQ_API_KEY` from environment.
- `app/engine/llm_client.py` — `SummarizationService` using the `groq` client.
- `app/engine/nlp_worker.py` — `SpacyProcessor` that extracts entities and compresses text.
- `app/messaging/messenger.py` — `MessageBroker` that reads `app/data/input_text.json` (simulates Kafka).
- `app/contract/schema.py` — `pydantic` input/output models and validators.
- `app/data/input_text.json` — sample input (used by `MessageBroker`).
- `app/data/system_prompt.txt` — optional system prompt for the LLM.
- `.env` — recommended local file to store `GROQ_API_KEY` (not committed).

Dependencies
------------
- `groq` — Groq API client used by `llm_client.py`.
- `pydantic` — data validation for contracts.
- `spacy` — NLP processing.
- `python-dotenv` — (optional) load `.env` from Python.

Environment variable
--------------------
The application requires a Groq API key named `GROQ_API_KEY`. Provide it either by exporting in your shell or by creating a `.env` file with:

GROQ_API_KEY=your_groq_api_key_here

Setup & Run (macOS / zsh)
-------------------------
1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Provide `GROQ_API_KEY`

Option A — export in the shell:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Option B — use `.env` and load it from Python (recommended):

Install `python-dotenv` (already in `requirements.txt`) and add this near the top of `run.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

Or source the file into your shell temporarily:

```bash
set -a
source .env
set +a
```

4. Install spaCy model (the code falls back to `en_core_web_sm` if `en_core_web_trf` is not installed):

```bash
python -m spacy download en_core_web_sm
# Optional: for transformer-based model (requires extra deps)
python -m spacy download en_core_web_trf
```

5. Run the app

```bash
python run.py
```

Notes & Troubleshooting
-----------------------
- If the script prints `GROQ_API_KEY: None` or the Groq client errors, verify the env var is exported or `load_dotenv()` is called before `app/engine/api.py` reads the env.
- Ensure you run `python run.py` from the repository root so relative paths (e.g. `app/data/input_text.json`) resolve correctly.
- If `app/data/input_text.json` is missing, `MessageBroker.get_message_from_producer()` returns `None` and nothing will run.

Security
--------
- Do NOT commit `.env` or secret keys to source control. Add `.env` to `.gitignore`.
- If a key was committed, rotate/revoke it immediately and purge history if necessary.

Optional next steps
-------------------
- Add a `load_dotenv()` call at the top of `run.py` to automatically load `.env`.
- Add `.env` to `.gitignore`.
- Add a small `README` section in the repo to describe how to get a Groq key and any billing/quotas.

