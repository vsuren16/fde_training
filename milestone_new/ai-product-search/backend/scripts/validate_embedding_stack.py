import asyncio
from pathlib import Path

from app.infrastructure.embedding.manager import EmbeddingManager


async def main() -> None:
    manager = EmbeddingManager()
    sample = "traditional temple outfit"
    vector = await manager.embed(sample)
    Path("scripts").mkdir(exist_ok=True)
    Path("scripts/embedding_probe.txt").write_text(str(len(vector)), encoding="utf-8")
    await manager.close()


if __name__ == "__main__":
    asyncio.run(main())
