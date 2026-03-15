# from app.db.chroma_client import get_products_collection, get_reviews_collection

# p = get_products_collection()
# r = get_reviews_collection()

# print("products:", p.name)
# print("reviews:", r.name)

#############

# from app.recommendations.review_text_builder import build_review_text_agg

# sample = {
#     "title": "Example Product",
#     "reviews": [
#         {"text": "Works great, battery lasts long."},
#         {"text": "Good value, but the buttons feel cheap."},
#     ]
# }

# print(build_review_text_agg(sample))

#################

from app.llm.embeddings import embed_text

v = embed_text("hello world")
print(type(v), len(v))
print(v[:5])