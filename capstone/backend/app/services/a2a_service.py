from __future__ import annotations

from app.schemas.incident import AgentMessage


class A2AService:
    def build_messages(self, handoff_path: list[str], query: str, incidents: list[dict]) -> list[AgentMessage]:
        if len(handoff_path) < 2:
            return []
        top = incidents[0] if incidents else {}
        messages: list[AgentMessage] = []
        for source, destination in zip(handoff_path, handoff_path[1:]):
            messages.append(
                AgentMessage(
                    from_agent=source,
                    to_agent=destination,
                    message=(
                        f"Sharing context for query '{query}'. "
                        f"Top incident {top.get('incident_id', 'N/A')} suggests "
                        f"{top.get('category', 'general troubleshooting')} owned by "
                        f"{top.get('team', 'the current team')}."
                    ),
                )
            )
        return messages
