from fastapi import HTTPException


def validate_query_text(query: str) -> str:
    normalized = query.strip()
    if not normalized:
        raise HTTPException(status_code=422, detail="query must not be empty")
    if len(normalized) < 8:
        raise HTTPException(
            status_code=422,
            detail="query is too short to retrieve meaningful incidents",
        )
    if len(normalized) > 2000:
        raise HTTPException(status_code=422, detail="query exceeds max length")
    return normalized
