import random
import asyncio
import json

from database import get_db
from classes.weight_classes import Worker
from classes.chat_classes import UserNeeds


def calculate_worker_score(worker: Worker, user_needs: UserNeeds) -> float:
    expertise_score = 0.0
    pricing_score = 0.0
    score = 0.0

    # Rating score based on global_rating and total_reviews
    rating_weight = 0
    rating_value = 0.0

    if worker.total_reviews >= 100:
        rating_weight = 100
        rating_value = worker.global_rating
    elif worker.total_reviews > 75:
        rating_weight = 90
        rating_value = worker.global_rating
    elif worker.total_reviews > 25:
        rating_weight = 70
        rating_value = worker.global_rating
    elif worker.total_reviews > 10:
        rating_weight = 60
        rating_value = worker.global_rating
    elif worker.global_rating >= 3.5:
        rating_weight = 60
        rating_value = worker.global_rating
    else:
        rating_weight = 60
        rating_value = 3.5

    # Expertise score from rating and badges
    expertise_score += rating_weight * (rating_value / 5.0)
    expertise_score += len(worker.badges) * 0.5

    # Pricing score based on price_from / price_to vs user range
    if worker.price_to <= user_needs.user_price_range[1]:
        pricing_score = 1.5
    else:
        pricing_score = 1.0

    if worker.price_from <= user_needs.user_price_range[0]:
        pricing_score += 1.5
    else:
        pricing_score += 1.0

    # If worker has subcategory matching user needs, boost score
    if user_needs.subcategory:
        full_subcat = f"{user_needs.category}.{user_needs.subcategory}"
        if full_subcat in worker.categories:
            expertise_score += 2.5


    # Combine scores
    score += expertise_score / 10.0 - user_needs.user_expected_expertise
    score = max(score, 0.0)
    score += pricing_score
    score = min(score, 10.0)
    score = round(score, 2)

    return score

def load_workers_from_json(filepath: str) -> list[Worker]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Worker(**w) for w in data]

async def load_workers_from_db() -> list[Worker]:
    db = get_db()
    data = await db.trabajadores.find().to_list(1000)
    return [Worker(**w) for w in data]

def filter_by_category(workers: list[Worker], category: str) -> list[Worker]:
    return [
        w for w in workers
        if any(c == category or c.startswith(f"{category}.") for c in w.categories)
    ]

def rank_workers(workers: list[Worker], user_needs: UserNeeds) -> list[tuple[Worker, float]]:
    scored = [(w.id, calculate_worker_score(w, user_needs)) for w in workers]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

def output_workers(
    workers: list[Worker],
    category: str,
    expertise: float,
    budget: tuple[int, int],
) -> dict:
    user_needs = UserNeeds()
    user_needs.user_expected_expertise = expertise
    user_needs.user_price_range = budget
    user_needs.category = category

    filtered = filter_by_category(workers, category)
    ranked = rank_workers(filtered, user_needs)

    return ranked[:3]