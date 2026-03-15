import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings
from app.core.langsmith import configure_langsmith
from app.core.logging import configure_logging
from app.infrastructure.auth.repositories import InMemoryOrderRepository, InMemorySessionRepository, InMemoryUserRepository
from app.infrastructure.db.session import init_db
from app.infrastructure.embedding.manager import EmbeddingManager
from app.infrastructure.mongodb.client import MongoClientManager
from app.infrastructure.auth.mongo_repositories import MongoOrderRepository, MongoUserRepository
from app.infrastructure.mongodb.in_memory_product_repository import InMemoryProductRepository
from app.infrastructure.mongodb.product_repository import MongoProductRepository
from app.infrastructure.vector_store.chroma_store import ChromaVectorStore
from app.infrastructure.vector_store.in_memory import InMemoryVectorStore
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService
from app.services.container import ServiceContainer
from app.services.ingestion_service import IngestionService
from app.services.keyword_search_service import KeywordSearchService
from app.services.llm_service import LLMService
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.recommendation_service import RecommendationService

configure_logging()
configure_langsmith()
logger = logging.getLogger(__name__)


async def _bootstrap_search_assets(app: FastAPI) -> None:
    container = app.state.container
    try:
        await container.ingestion_service.build_index()
        logger.info("product_index_ready")
    except Exception:
        logger.exception("product_index_bootstrap_failed")

    try:
        await container.chat_service.bootstrap_policy_knowledge()
        logger.info("policy_index_ready")
    except Exception:
        logger.exception("policy_index_bootstrap_failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_repo = InMemorySessionRepository()
    user_repo = InMemoryUserRepository()
    order_repo = InMemoryOrderRepository()

    mongo_manager = MongoClientManager()
    try:
        db = await mongo_manager.connect()
        product_repository = MongoProductRepository.from_database(db)
        user_repo = MongoUserRepository.from_database(db)
        order_repo = MongoOrderRepository.from_database(db)
        await user_repo.create_indexes()
        await order_repo.create_indexes()
    except Exception:
        logger.warning("mongodb_unavailable_using_in_memory")
        product_repository = InMemoryProductRepository()

    auth_service = AuthService(user_repo, session_repo)
    order_service = OrderService(order_repo)
    await auth_service.ensure_admin()
    product_service = ProductService(product_repository)
    await product_service.initialize()
    await product_service.ensure_seed_data(settings.seed_products_count)

    embedding_manager = EmbeddingManager()
    llm_service = LLMService()
    try:
        vector_store = ChromaVectorStore(
            persist_dir=settings.chroma_persist_dir,
            collection_name=settings.chroma_products_collection,
        )
    except Exception:
        logger.warning("chroma_unavailable_using_in_memory_vector_store")
        vector_store = InMemoryVectorStore()
    ingestion_service = IngestionService(product_service, embedding_manager, vector_store)
    keyword_search_service = KeywordSearchService()
    recommendation_service = RecommendationService(
        embedding_manager=embedding_manager,
        vector_store=vector_store,
        product_service=product_service,
        keyword_search_service=keyword_search_service,
        llm_service=llm_service,
    )

    await init_db()
    policy_store = ChromaVectorStore(
        persist_dir=settings.chroma_persist_dir,
        collection_name=settings.chroma_policy_collection,
    )
    chat_service = ChatService(
        embedding_manager=embedding_manager,
        product_vector_store=vector_store,
        order_service=order_service,
        policy_vector_store=policy_store,
        llm_service=llm_service,
    )

    app.state.container = ServiceContainer(
        product_service=product_service,
        auth_service=auth_service,
        order_service=order_service,
        embedding_manager=embedding_manager,
        vector_store=vector_store,
        ingestion_service=ingestion_service,
        recommendation_service=recommendation_service,
        chat_service=chat_service,
        llm_service=llm_service,
        mongo_manager=mongo_manager,
    )
    app.state.bootstrap_task = asyncio.create_task(_bootstrap_search_assets(app))

    logger.info(
        "startup_complete",
        extra={"configured_model_chain": embedding_manager.configured_model_chain},
    )
    yield
    bootstrap_task = getattr(app.state, "bootstrap_task", None)
    if bootstrap_task:
        bootstrap_task.cancel()
        try:
            await bootstrap_task
        except asyncio.CancelledError:
            pass
    await llm_service.close()
    await embedding_manager.close()
    await mongo_manager.close()


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")
