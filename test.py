# test_filter_and_score.py
import asyncio
import json
from classes.weight_classes import Worker
from functions.weight_functions import calculate_worker_score, UserNeeds
from database import get_db


def load_workers_from_json(filepath: str) -> list[Worker]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Worker(**w) for w in data]


async def load_workers_from_db() -> list[Worker]:
    db = get_db()
    data = await db.tecnicos.find().to_list(1000)
    return [Worker(**w) for w in data]


def filter_by_category(workers: list[Worker], category: str) -> list[Worker]:
    return [
        w for w in workers
        if any(c == category or c.startswith(f"{category}.") for c in w.categories)
    ]


def rank_workers(workers: list[Worker], user_needs: UserNeeds) -> list[tuple[Worker, float]]:
    scored = [(w, calculate_worker_score(w, user_needs)) for w in workers]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def build_result_json(ranked: list[tuple[Worker, float]]) -> dict:
    """Build the output JSON with worker IDs and their scores in order."""
    return {
        "proveedores_sugeridos": [worker.id for worker, _ in ranked],
        "calificaciones": [round(score, 2) for _, score in ranked],
    }


def test_category(
    workers: list[Worker],
    category: str,
    expertise: float,
    budget: tuple[int, int],
) -> dict:
    user_needs = UserNeeds()
    user_needs.user_expertise = expertise
    user_needs.user_price_range = budget

    filtered = filter_by_category(workers, category)
    ranked = rank_workers(filtered, user_needs)
    return build_result_json(ranked)


async def run(use_db: bool = False):
    if use_db:
        print("Loading workers from MongoDB...")
        workers = await load_workers_from_db()
    else:
        print("Loading workers from JSON...")
        workers = load_workers_from_json("trabajadores.json")

    result = test_category(workers, category="plomeria", expertise=4.0, budget=(300, 800))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


if __name__ == "__main__":
    asyncio.run(run(use_db=True))