# VeriForge AI

Trustworthy multi-agent AI reasoning and verification engine.

## Pipeline
User Task → Planner → Specialized Agents → Evidence → Independent Verification → Contradiction/Risk Detection → Self-Correction → Finalizer → Audit

## Features
- Specialized planner, researcher, coder/tool-use, verifier, critic and finalizer agents
- Evidence-grounded claims
- Independent factual, logical, computational and tool verification
- Contradiction and unsupported-claim detection
- Self-correction and re-verification
- Audit trail with confidence and rejection reasons
- Evaluation set for ambiguous, incomplete, conflicting and misleading inputs

## Demo
Run:
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Then open `http://127.0.0.1:8000`.

## Repository
Push this project to a public GitHub repository and add the deployed URL here before submission.
