from .agents.planner import plan
from .agents.researcher import research
from .agents.coder import tool_check
from .agents.verifier import verify
from .agents.critic import critique
from .agents.finalizer import finalize

from .risk_detector import detect_risk
from .audit import save_audit_log


# ---------------------------------------------------------
# Check whether an AI call failed
# ---------------------------------------------------------

def ai_service_failed(result):

    if not result:
        return False

    text = str(result).upper()

    return "AI SERVICE ERROR" in text


# ---------------------------------------------------------
# Decide whether the task needs full verification
# ---------------------------------------------------------

def is_complex_task(task):

    text = task.lower()

    complex_keywords = [

        # Programming
        "code",
        "program",
        "python",
        "java",
        "javascript",
        "c++",
        "sql",
        "algorithm",
        "debug",
        "bug",
        "function",
        "api",

        # Mathematics
        "calculate",
        "solve",
        "equation",
        "multiply",
        "divide",
        "percentage",
        "probability",
        "formula",
        "math",

        # Reasoning
        "prove",
        "compare",
        "analyze",
        "analyse",
        "reason",
        "derive",
        "step by step",

        # High verification need
        "medical",
        "legal",
        "security",
        "financial",
        "safety",
        "risk"
    ]

    for keyword in complex_keywords:

        if keyword in text:
            return True

    return False


# ---------------------------------------------------------
# Fast mode
# ---------------------------------------------------------

def run_fast_mode(task, plan_result, evidence_result):

    print("\nFAST VERIFICATION MODE")

    # -----------------------------------------------------
    # Candidate generation
    # -----------------------------------------------------

    print("\n[3/5] Coder Agent working...")

    tool_result = tool_check(
        task,
        plan_result
    )

    print("Candidate answer generated.")

    # -----------------------------------------------------
    # Verification
    # -----------------------------------------------------

    print("\n[4/5] Verifier Agent working...")

    verification = verify(
        task,
        evidence_result["evidence"],
        tool_result["result"]
    )

    print(
        "Verification:",
        verification["status"]
    )

    # -----------------------------------------------------
    # If verification fails, retry once
    # -----------------------------------------------------

    if verification["status"] != "passed":

        print(
            "\nVerification failed."
        )

        print(
            "Running one correction attempt..."
        )

        corrected_task = f"""
Original task:

{task}

The previous candidate answer failed
verification.

Create a corrected answer.

Carefully check:

- factual accuracy
- calculations
- reasoning
- code
- assumptions
- evidence

Return a new candidate answer.
"""

        tool_result = tool_check(
            corrected_task,
            plan_result
        )

        verification = verify(
            task,
            evidence_result["evidence"],
            tool_result["result"]
        )

        print(
            "Second verification:",
            verification["status"]
        )

    # -----------------------------------------------------
    # Finalizer
    # -----------------------------------------------------

    print("\n[5/5] Finalizer Agent working...")

    if verification["status"] == "passed":

        final = finalize(
            task,
            plan_result,
            evidence_result["evidence"],
            tool_result["result"],
            verification,
            {
                "risk": "low",
                "critique":
                    "Fast verification mode."
            }
        )

    else:

        final = {
            "agent": "finalizer",
            "status": "rejected",
            "answer": None,
            "message":
                "The candidate answer could not "
                "be independently verified."
        }

    return {
        "tool_result": tool_result,
        "verification": verification,
        "critique": {
            "agent": "critic",
            "risk": "low",
            "critique":
                "Fast verification mode used."
        },
        "risk": {
            "agent": "risk_detector",
            "risk": "low",
            "analysis":
                "Fast verification mode used."
        },
        "final": final
    }


# ---------------------------------------------------------
# Full verification mode
# ---------------------------------------------------------

def run_full_mode(task, plan_result, evidence_result):

    print("\nFULL VERIFICATION MODE")

    max_attempts = 2

    attempt = 1

    tool_result = None
    verification = None

    # -----------------------------------------------------
    # Candidate + verification loop
    # -----------------------------------------------------

    while attempt <= max_attempts:

        print(
            f"\n[3/7] Coder Agent working - "
            f"Attempt {attempt}..."
        )

        current_task = task

        if attempt > 1:

            current_task = f"""
Original task:

{task}

The previous candidate answer failed
independent verification.

Create a corrected answer.

Carefully check:

- calculations
- reasoning
- factual claims
- code
- assumptions
- evidence

Produce a new candidate answer.
"""

        tool_result = tool_check(
            current_task,
            plan_result
        )

        if ai_service_failed(
            tool_result.get("result")
        ):

            break

        print(
            "Candidate answer generated."
        )

        # -------------------------------------------------
        # Verification
        # -------------------------------------------------

        print(
            f"[4/7] Verifier Agent working - "
            f"Attempt {attempt}..."
        )

        verification = verify(
            task,
            evidence_result["evidence"],
            tool_result["result"]
        )

        print(
            "Verification:",
            verification["status"]
        )

        if verification["status"] == "passed":

            print(
                "Verification passed."
            )

            break

        print(
            "Verification failed."
        )

        attempt += 1

    # -----------------------------------------------------
    # AI failure
    # -----------------------------------------------------

    if (
        tool_result is None
        or ai_service_failed(
            tool_result.get("result")
        )
    ):

        verification = {
            "agent": "verifier",
            "status": "failed",
            "verification":
                "AI service unavailable."
        }

        criticism = {
            "agent": "critic",
            "risk": "high",
            "critique":
                "AI service unavailable."
        }

        risk_result = {
            "agent": "risk_detector",
            "risk": "high",
            "analysis":
                "AI service unavailable."
        }

        final = {
            "agent": "finalizer",
            "status": "rejected",
            "answer": None,
            "message":
                "The AI service became unavailable."
        }

        return {
            "tool_result":
                tool_result or {
                    "result": None
                },

            "verification":
                verification,

            "critique":
                criticism,

            "risk":
                risk_result,

            "final":
                final
        }

    # -----------------------------------------------------
    # Critic
    # -----------------------------------------------------

    print(
        "\n[5/7] Critic Agent working..."
    )

    criticism = critique(
        task,
        evidence_result["evidence"],
        tool_result["result"],
        verification["verification"]
    )

    print(
        "Critic Risk:",
        criticism["risk"]
    )

    # -----------------------------------------------------
    # Risk detector
    # -----------------------------------------------------

    print(
        "\n[6/7] Risk & Contradiction Detector working..."
    )

    risk_result = detect_risk(
        task,
        evidence_result["evidence"],
        tool_result["result"]
    )

    print(
        "Detected Risk:",
        risk_result["risk"]
    )

    # -----------------------------------------------------
    # Finalizer
    # -----------------------------------------------------

    print(
        "\n[7/7] Finalizer Agent working..."
    )

    if (
        verification["status"] != "passed"
        or criticism["risk"] == "high"
        or risk_result["risk"] == "high"
    ):

        final = {
            "agent": "finalizer",
            "status": "rejected",
            "answer": None,
            "message":
                "Answer rejected because "
                "verification or risk checks failed."
        }

    else:

        final = finalize(
            task,
            plan_result,
            evidence_result["evidence"],
            tool_result["result"],
            verification,
            criticism
        )

    return {
        "tool_result":
            tool_result,

        "verification":
            verification,

        "critique":
            criticism,

        "risk":
            risk_result,

        "final":
            final
    }


# ---------------------------------------------------------
# MAIN ORCHESTRATOR
# ---------------------------------------------------------

def run_task(task):

    print("\n================================")
    print("VERIFORGE AI")
    print("MULTI-AGENT REASONING ENGINE")
    print("================================")

    task = task.strip()

    if not task:

        return {
            "task": task,

            "plan": {},

            "evidence": {
                "status": "insufficient",
                "sources": []
            },

            "tool_result": {
                "result": None
            },

            "verification": {
                "status": "failed",
                "verification":
                    "Empty task."
            },

            "critique": {
                "risk": "high",
                "critique":
                    "No task was provided."
            },

            "risk": {
                "risk": "high",
                "analysis":
                    "No task was provided."
            },

            "final": {
                "status": "rejected",
                "answer": None,
                "message":
                    "Please enter a task."
            },

            "attempts": 0
        }


    # =====================================================
    # 1. PLANNER
    # =====================================================

    print(
        "\n[1] Planner Agent working..."
    )

    plan_result = plan(task)

    print(
        "Planner completed."
    )


    # -----------------------------------------------------
    # Check AI failure
    # -----------------------------------------------------

    if ai_service_failed(
        plan_result.get("plan")
    ):

        result = {

            "task": task,

            "plan":
                plan_result,

            "evidence": {
                "status": "not_started",
                "sources": []
            },

            "tool_result": {
                "result": None
            },

            "verification": {
                "status": "failed",
                "verification":
                    "AI service unavailable."
            },

            "critique": {
                "risk": "high",
                "critique":
                    "AI service unavailable."
            },

            "risk": {
                "risk": "high",
                "analysis":
                    "AI service unavailable."
            },

            "final": {
                "agent": "finalizer",
                "status": "rejected",
                "answer": None,
                "message":
                    "AI service unavailable."
            },

            "attempts": 0
        }

        save_audit_log(result)

        return result


    # =====================================================
    # 2. RESEARCHER
    # =====================================================

    print(
        "\n[2] Researcher Agent working..."
    )

    evidence_result = research(
        task,
        plan_result
    )

    print(
        "Research completed."
    )


    # =====================================================
    # SELECT MODE
    # =====================================================

    if is_complex_task(task):

        print(
            "\nTask classified as COMPLEX."
        )

        result_data = run_full_mode(
            task,
            plan_result,
            evidence_result
        )

    else:

        print(
            "\nTask classified as SIMPLE."
        )

        result_data = run_fast_mode(
            task,
            plan_result,
            evidence_result
        )


    # =====================================================
    # BUILD FINAL RESULT
    # =====================================================

    result = {

        "task":
            task,

        "plan":
            plan_result,

        "evidence":
            evidence_result,

        "tool_result":
            result_data["tool_result"],

        "verification":
            result_data["verification"],

        "critique":
            result_data["critique"],

        "risk":
            result_data["risk"],

        "final":
            result_data["final"],

        "attempts":
            1
    }


    # =====================================================
    # AUDIT LOG
    # =====================================================

    save_audit_log(result)


    # =====================================================
    # TERMINAL OUTPUT
    # =====================================================

    print("\n================================")
    print("FINAL RESULT")
    print("================================")

    print(
        "Verification:",
        result["verification"]["status"]
    )

    print(
        "Critic Risk:",
        result["critique"]["risk"]
    )

    print(
        "Detected Risk:",
        result["risk"]["risk"]
    )

    print(
        "Final Status:",
        result["final"]["status"]
    )


    if result["final"].get("answer"):

        print("\nFINAL ANSWER:")

        print(
            result["final"]["answer"]
        )

    else:

        print("\nREASON:")

        print(
            result["final"].get(
                "message",
                "Answer was rejected."
            )
        )


    print(
        "\nAudit log saved to audit_log.json"
    )


    return result


# =========================================================
# DIRECT TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    task = input(
        "\nEnter your task: "
    )

    run_task(task)