from __future__ import annotations

from app.core.container import get_incident_repository, get_openai_adapter, get_vector_store
from app.observability.langsmith import traced
from app.observability.logging import get_logger
from app.services.dataset_materialization_service import DatasetMaterializationService
from app.services.keyword_search_service import KeywordSearchService


logger = get_logger(__name__)


class IndexingService:
    def __init__(self, keyword_search_service: KeywordSearchService) -> None:
        self.dataset_service = DatasetMaterializationService()
        self.repository = get_incident_repository()
        self.openai = get_openai_adapter()
        self.vector_store = get_vector_store()
        self.keyword_search_service = keyword_search_service

    @traced(run_type="chain", name="incident_ingestion")
    def ingest(self, batch_size: int | None = None) -> dict:
        batch_size = batch_size or self.dataset_service.settings.embedding_batch_size
        logger.info(
            "ingestion_started",
            extra={
                "raw_dataset_path": str(self.dataset_service.settings.raw_dataset_path),
                "processed_dataset_path": str(self.dataset_service.settings.processed_dataset_path),
                "batch_size": batch_size,
            },
        )
        output_path = self.dataset_service.write_processed_dataset()
        incidents = self.dataset_service.load_processed_incidents()
        logger.info(
            "mongo_replace_started",
            extra={"records_to_load": len(incidents)},
        )
        self.repository.ensure_indexes()
        upserted = self.repository.replace_all(incidents)
        logger.info(
            "mongo_replace_completed",
            extra={
                "records_loaded": len(incidents),
                "records_upserted": upserted,
                "documents_in_mongo": self.repository.count(),
            },
        )
        embeddings_indexed = 0
        vector_mode = "disabled"
        logger.info("chroma_reset_started")
        self.vector_store.reset()
        logger.info("chroma_reset_completed", extra={"vectors_in_chroma": self.vector_store.count()})

        if self.openai.enabled:
            vector_mode = "openai_embeddings"
            logger.info(
                "embedding_indexing_started",
                extra={"records_to_embed": len(incidents), "batch_size": batch_size},
            )
            total_batches = max((len(incidents) + batch_size - 1) // batch_size, 1)
            for start in range(0, len(incidents), batch_size):
                batch = incidents[start : start + batch_size]
                batch_number = (start // batch_size) + 1
                logger.info(
                    "embedding_batch_started",
                    extra={
                        "batch_number": batch_number,
                        "total_batches": total_batches,
                        "batch_records": len(batch),
                        "batch_start_offset": start,
                    },
                )
                documents = [
                    f"Title: {item['title']}\nDescription: {item['description']}\nResolution: {item['resolution_notes']}"
                    for item in batch
                ]
                embeddings = self.openai.embed_texts(documents)
                self.vector_store.upsert(
                    ids=[item["incident_id"] for item in batch],
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=[
                        {
                            key: value
                            for key, value in {
                                "priority": item.get("priority"),
                                "category": item.get("category"),
                                "status": item.get("status"),
                                "team": item.get("team"),
                            }.items()
                            if value is not None
                        }
                        for item in batch
                    ],
                )
                embeddings_indexed += len(batch)
                logger.info(
                    "embedding_batch_completed",
                    extra={
                        "batch_number": batch_number,
                        "total_batches": total_batches,
                        "embeddings_indexed": embeddings_indexed,
                    },
                )
            logger.info(
                "embedding_indexing_completed",
                extra={
                    "embeddings_indexed": embeddings_indexed,
                    "vectors_in_chroma": self.vector_store.count(),
                },
            )
        else:
            logger.warning("vector_indexing_skipped", extra={"reason": "missing_openai_key"})

        logger.info("keyword_index_load_started", extra={"records_to_index": len(incidents)})
        self.keyword_search_service.load(incidents)
        result = {
            "processed_dataset_path": str(output_path),
            "documents_in_mongo": self.repository.count(),
            "vectors_in_chroma": self.vector_store.count(),
            "records_upserted": upserted,
            "embeddings_indexed": embeddings_indexed,
            "vector_mode": vector_mode,
        }
        logger.info("ingestion_completed", extra=result)
        return result
