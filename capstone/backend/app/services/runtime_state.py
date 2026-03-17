from functools import lru_cache

from app.services.keyword_search_service import KeywordSearchService
from app.services.search_service import SearchService
from app.services.search_diagnostics_service import SearchDiagnosticsService


@lru_cache
def get_keyword_search_service() -> KeywordSearchService:
    return KeywordSearchService()


@lru_cache
def get_search_service() -> SearchService:
    return SearchService(get_keyword_search_service())


@lru_cache
def get_search_diagnostics_service() -> SearchDiagnosticsService:
    return SearchDiagnosticsService()
