# Architecture

## Agent responsibilities
1. Planner — decomposes the task.
2. Researcher — retrieves evidence and attaches it to claims.
3. Coder/Tool Agent — performs calculations, API checks and sandboxed execution.
4. Independent Verifier — checks claims through a separate path.
5. Critic — searches for contradictions, unsupported claims and risks.
6. Finalizer — accepts, requests correction, or rejects.

## Verification loop

Generation → Verification → Failure classification → Correction → Re-verification → Acceptance/Rejection.

Generation quality and verification quality are measured separately.
