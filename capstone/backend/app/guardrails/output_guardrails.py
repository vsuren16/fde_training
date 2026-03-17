from app.schemas.incident import SearchResponse


def validate_grounded_response(response: SearchResponse) -> SearchResponse:
    if response.resolution_summary and not response.incidents:
        response.degraded = True
    if response.judge_status in {"degraded", "blocked"}:
        response.degraded = True
    return response
