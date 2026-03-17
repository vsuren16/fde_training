from app.evaluation.judge_service import JudgeService


class DisabledOpenAIAdapter:
    enabled = False


def test_judge_blocks_weakly_grounded_answer() -> None:
    service = JudgeService(DisabledOpenAIAdapter())
    verdict = service.evaluate(
        query="Users cannot connect remotely",
        incidents=[
            {
                "title": "Citrix access denied",
                "description": "Users cannot connect to Citrix remotely with valid credentials.",
                "incident_text": "Citrix remote access denied for valid users.",
                "resolution_notes": "Restart Citrix service and validate access policy.",
                "category": "Network",
                "team": "Network Operations",
            }
        ],
        answer="Replace the desktop monitor and change printer toner.",
    )

    assert verdict.approved is False
    assert verdict.status in {"degraded", "blocked"}


def test_judge_approves_grounded_answer() -> None:
    service = JudgeService(DisabledOpenAIAdapter())
    verdict = service.evaluate(
        query="Users cannot connect remotely",
        incidents=[
            {
                "title": "Citrix access denied",
                "description": "Users cannot connect to Citrix remotely with valid credentials.",
                "incident_text": "Citrix remote access denied for valid users.",
                "resolution_notes": "Restart Citrix service and validate access policy.",
                "category": "Network",
                "team": "Network Operations",
            }
        ],
        answer="Review the Citrix service, validate access policy, and confirm the software path for remote connectivity.",
    )

    assert verdict.approved is True
    assert verdict.status == "approved"
