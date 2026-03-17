from __future__ import annotations


class AgentHandoffService:
    def handoff_path(self, triage_priority: int | None, incidents: list[dict]) -> list[str]:
        if not incidents:
            return ["L1_SUPPORT"]

        top = incidents[0]
        category = str(top.get("category") or "application").lower()
        base = ["L1_SUPPORT"]
        if category in {"network", "security"}:
            base.append("L2_INFRA")
            if triage_priority in {1, 2}:
                base.append("L3_NETWORK_SPECIALIST")
            return base
        if category in {"database", "storage"}:
            base.append("L2_PLATFORM")
            if triage_priority in {1, 2}:
                base.append("L3_PLATFORM_SPECIALIST")
            return base
        if category == "hardware":
            base.append("FIELD_SUPPORT")
            if triage_priority in {1, 2}:
                base.append("L3_HARDWARE_SPECIALIST")
            return base
        if triage_priority in {1, 2}:
            base.append("L2_APPLICATION")
            base.append("L3_APPLICATION_SPECIALIST")
            return base
        base.append("L2_APPLICATION")
        return base
