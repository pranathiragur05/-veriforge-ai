import json
from datetime import datetime


def create_audit_log(result):

    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "task": result["task"],

        "verification": {
            "status": result["verification"]["status"],
            "details": result["verification"]["verification"]
        },

        "critique": {
            "risk": result["critique"]["risk"],
            "details": result["critique"]["critique"]
        },

        "risk_detection": {
            "risk": result["risk"]["risk"],
            "details": result["risk"]["analysis"]
        },

        "correction_attempts": result["attempts"],

        "final_decision": {
            "status": result["final"]["status"],
            "answer": result["final"].get("answer"),
            "message": result["final"].get("message")
        }
    }

    return audit_record


def save_audit_log(result):

    audit_record = create_audit_log(result)

    with open(
        "audit_log.json",
        "a",
        encoding="utf-8"
    ) as file:

        json.dump(
            audit_record,
            file,
            indent=4,
            ensure_ascii=False
        )

        file.write("\n")

    return audit_record