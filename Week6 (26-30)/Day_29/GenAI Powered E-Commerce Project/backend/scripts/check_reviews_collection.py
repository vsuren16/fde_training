from app.db.chroma_client import get_reviews_collection

c = get_reviews_collection()
print("collection:", c.name)
print("count:", c.count())