from __future__ import annotations


class RoutingService:
    def route(self, incidents: list[dict]) -> str:
        if not incidents:
            return "L1_SUPPORT"
        top = incidents[0]
        category = str(top.get("category") or "application").lower()
        team = str(top.get("team") or "").lower()
        if category == "database" or "database" in team or "platform" in team:
            return "L2_PLATFORM"
        if category in {"network", "security"} or "network" in team:
            return "L2_INFRA"
        if category == "hardware":
            return "FIELD_SUPPORT"
        return "L2_APPLICATION"
