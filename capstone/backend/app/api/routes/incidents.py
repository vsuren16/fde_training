from fastapi import APIRouter

from app.core.container import get_incident_repository, get_vector_store
from app.observability.logging import get_logger
from app.schemas.incident import (
    EvaluationResponse,
    FeedbackRequest,
    FeedbackResponse,
    IngestionPreviewResponse,
    IngestionRunResponse,
    IngestionStatusResponse,
    MetadataOptionsResponse,
    SearchRequest,
    SearchResponse,
)
from app.evaluation.deepeval_service import DeepEvalService
from app.services.feedback_service import FeedbackService
from app.services.indexing_service import IndexingService
from app.services.ingestion_service import IngestionService
from app.services.runtime_state import get_keyword_search_service, get_search_service


router = APIRouter()
logger = get_logger(__name__)


@router.get("/ingestion/preview", response_model=IngestionPreviewResponse)
async def preview_ingestion() -> IngestionPreviewResponse:
    service = IngestionService()
    return service.preview_dataset()


@router.post("/ingestion/load", response_model=IngestionRunResponse)
async def run_ingestion() -> IngestionRunResponse:
    logger.info("ingestion_request_received")
    service = IndexingService(get_keyword_search_service())
    response = IngestionRunResponse.model_validate(service.ingest())
    logger.info(
        "ingestion_request_completed",
        extra={
            "documents_in_mongo": response.documents_in_mongo,
            "vectors_in_chroma": response.vectors_in_chroma,
            "vector_mode": response.vector_mode,
        },
    )
    return response


@router.get("/ingestion/status", response_model=IngestionStatusResponse)
async def ingestion_status() -> IngestionStatusResponse:
    repository = get_incident_repository()
    vector_store = get_vector_store()
    return IngestionStatusResponse(
        documents_in_mongo=repository.count(),
        vectors_in_chroma=vector_store.count(),
        keyword_index_loaded=get_keyword_search_service().is_loaded(),
    )


@router.get("/metadata/options", response_model=MetadataOptionsResponse)
async def metadata_options() -> MetadataOptionsResponse:
    repository = get_incident_repository()
    return MetadataOptionsResponse(
        categories=repository.distinct_values("category"),
        teams=repository.distinct_values("team"),
    )


@router.post("/search", response_model=SearchResponse)
async def search_incidents(payload: SearchRequest) -> SearchResponse:
    return get_search_service().search(payload)


@router.post("/feedback", response_model=FeedbackResponse)
async def store_feedback(payload: FeedbackRequest) -> FeedbackResponse:
    return FeedbackService().store(payload)


@router.get("/evaluation/deepeval", response_model=EvaluationResponse)
async def deepeval_status() -> EvaluationResponse:
    return DeepEvalService().run()
