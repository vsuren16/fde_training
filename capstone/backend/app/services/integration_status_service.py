from __future__ import annotations

from langsmith import Client as LangSmithClient

from app.adapters.openai_adapter import OpenAIAdapter
from app.adapters.chroma_adapter import ChromaVectorStore, NoOpVectorStore
from app.core.config import get_settings
from app.repositories.mongo_repository import get_mongo_client
from app.schemas.admin import IntegrationStatus


class IntegrationStatusService:
    def __init__(self, openai_adapter: OpenAIAdapter, vector_store: ChromaVectorStore | NoOpVectorStore) -> None:
        self.settings = get_settings()
        self.openai_adapter = openai_adapter
        self.vector_store = vector_store

    def mongo_status(self) -> IntegrationStatus:
        configured = bool(self.settings.mongodb_uri)
        if not configured:
            return IntegrationStatus(
                configured=False,
                connected=False,
                detail="MongoDB URI is not configured.",
            )
        try:
            get_mongo_client().admin.command("ping")
            return IntegrationStatus(
                configured=True,
                connected=True,
                detail="MongoDB ping succeeded.",
            )
        except Exception as exc:
            return IntegrationStatus(
                configured=True,
                connected=False,
                detail=f"MongoDB ping failed: {exc}",
            )

    def openai_status(self) -> IntegrationStatus:
        configured = self.openai_adapter.enabled
        if not configured:
            return IntegrationStatus(
                configured=False,
                connected=False,
                detail="OpenAI API key is not configured.",
            )
        try:
            self.openai_adapter.check_connectivity()
            return IntegrationStatus(
                configured=True,
                connected=True,
                detail="OpenAI API key validated successfully.",
            )
        except Exception as exc:
            return IntegrationStatus(
                configured=True,
                connected=False,
                detail=f"OpenAI connectivity check failed: {exc}",
            )

    def langsmith_status(self) -> IntegrationStatus:
        configured = bool(self.settings.langsmith_api_key and self.settings.langsmith_tracing)
        if not configured:
            return IntegrationStatus(
                configured=False,
                connected=False,
                detail="LangSmith API key or tracing flag is not configured.",
            )
        try:
            client = LangSmithClient(
                api_key=self.settings.langsmith_api_key,
                api_url="https://api.smith.langchain.com",
            )
            next(iter(client.list_projects(limit=1)), None)
            return IntegrationStatus(
                configured=True,
                connected=True,
                detail="LangSmith connectivity check succeeded.",
            )
        except Exception as exc:
            return IntegrationStatus(
                configured=True,
                connected=False,
                detail=f"LangSmith connectivity check failed: {exc}",
            )

    def chroma_status(self) -> IntegrationStatus:
        configured = not isinstance(self.vector_store, NoOpVectorStore)
        if not configured:
            return IntegrationStatus(
                configured=False,
                connected=False,
                detail="Chroma vector store is not active in the current runtime.",
            )
        try:
            count = self.vector_store.count()
            return IntegrationStatus(
                configured=True,
                connected=True,
                detail=f"Chroma collection is reachable. Current vector count: {count}.",
            )
        except Exception as exc:
            return IntegrationStatus(
                configured=True,
                connected=False,
                detail=f"Chroma connectivity check failed: {exc}",
            )
