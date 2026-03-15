import random


SPORTS_ITEMS = [
    "Running Shoes",
    "Yoga Mat",
    "Football Jersey",
    "Cricket Bat",
    "Gym Gloves",
    "Water Bottle",
]
DRESS_ITEMS = [
    "Maxi Dress",
    "Kurti Set",
    "Evening Gown",
    "Denim Jacket",
    "Linen Shirt",
    "Formal Blazer",
]
STATIONERY_ITEMS = [
    "Premium Notebook",
    "Gel Pen Set",
    "Desk Organizer",
    "Sketch Marker Pack",
    "Sticky Notes Combo",
    "Academic Planner",
]
BRANDS = [
    "AeroFit",
    "UrbanThread",
    "ClassicWeave",
    "NoteCraft",
    "PeakMove",
    "WriteRight",
    "ZenSport",
    "DailyStyle",
]
COLORS = ["Black", "White", "Blue", "Red", "Green", "Grey", "Pink", "Navy", "Brown"]
SIZES = ["XS", "S", "M", "L", "XL", "XXL", "Free"]


def _image_keywords(category: str, item_name: str) -> str:
    item = item_name.lower()
    if category == "sports":
        if "shoes" in item:
            return "running-shoes,sneakers"
        if "mat" in item:
            return "yoga-mat,fitness"
        if "jersey" in item:
            return "sports-jersey"
        if "bat" in item:
            return "cricket-bat,sports"
        return "sports,fitness"
    if category == "dresses":
        if "dress" in item or "gown" in item:
            return "fashion-dress,woman"
        if "shirt" in item:
            return "linen-shirt,fashion"
        if "blazer" in item:
            return "blazer,formal-fashion"
        return "fashion,clothing"
    return "stationery,office-supplies"


def _image_set(category: str, item_name: str, idx: int) -> tuple[str, list[str]]:
    keywords = _image_keywords(category, item_name)
    base = "https://loremflickr.com"
    urls = [
        f"{base}/640/640/{keywords}?lock={idx * 3 + 1}",
        f"{base}/640/640/{keywords}?lock={idx * 3 + 2}",
        f"{base}/640/640/{keywords}?lock={idx * 3 + 3}",
    ]
    return urls[0], urls


def _dimensions() -> dict:
    return {
        "length_cm": round(random.uniform(10, 70), 1),
        "width_cm": round(random.uniform(10, 50), 1),
        "height_cm": round(random.uniform(1, 30), 1),
    }


def _reviews() -> list[dict]:
    snippets = [
        "Great quality for the price.",
        "Comfortable and durable.",
        "Looks exactly like the photos.",
        "Packaging was neat and secure.",
        "Worth buying again.",
    ]
    return [
        {
            "user": f"user_{random.randint(1000, 9999)}",
            "comment": random.choice(snippets),
            "rating": round(random.uniform(3.2, 5.0), 1),
        }
        for _ in range(random.randint(2, 5))
    ]


def generate_mock_products(count: int = 1000) -> list[dict]:
    random.seed(42)
    catalog = []
    for idx in range(count):
        if idx % 3 == 0:
            category = "sports"
            name = random.choice(SPORTS_ITEMS)
        elif idx % 3 == 1:
            category = "dresses"
            name = random.choice(DRESS_ITEMS)
        else:
            category = "stationaries"
            name = random.choice(STATIONERY_ITEMS)

        brand = random.choice(BRANDS)
        color = random.choice(COLORS)
        size = random.choice(SIZES)
        rating = round(random.uniform(3.0, 5.0), 1)
        price = round(random.uniform(199, 7999), 2)
        image_url, image_urls = _image_set(category, name, idx)

        catalog.append(
            {
                "id": f"p-{100000 + idx}",
                "product_name": f"{brand} {name}",
                "short_description": f"{name} in {color} for everyday usage.",
                "description": (
                    f"{brand} {name} built for {category}. "
                    f"Color: {color}, Size: {size}. "
                    "Designed for comfort, durability, and practical daily use."
                ),
                "category": category,
                "brand": brand,
                "color": color,
                "size": size,
                "price": price,
                "image_url": image_url,
                "image_urls": image_urls,
                "rating": rating,
                "dimensions": _dimensions(),
                "availability": random.random() > 0.08,
                "reviews": _reviews(),
            }
        )
    return catalog
