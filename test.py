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
    """Filter workers by main category (ignores subcategories like 'plumbing.leaks')."""
    return [
        w for w in workers
        if any(c == category or c.startswith(f"{category}.") for c in w.categories)
    ]


def rank_workers(workers: list[Worker], user_needs: UserNeeds) -> list[tuple[Worker, float]]:
    scored = [(w, calculate_worker_score(w, user_needs)) for w in workers]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def print_results(ranked: list[tuple[Worker, float]], category: str, user_needs: UserNeeds):
    print(f"\n{'='*60}")
    print(f"  Category : {category}")
    print(f"  Budget   : ${user_needs.user_price_range[0]} - ${user_needs.user_price_range[1]}")
    print(f"  Expertise: {user_needs.user_expertise}")
    print(f"{'='*60}")

    if not ranked:
        print("  No workers found for this category.")
        return

    for i, (worker, score) in enumerate(ranked):
        available = "✓" if worker.available else "✗"
        print(
            f"  #{i+1:<3} {worker.name:<25} "
            f"[{available}] "
            f"★ {worker.global_rating} ({worker.total_reviews} reviews) | "
            f"badges: {len(worker.badges)} | "
            f"${worker.price_from}-${worker.price_to} | "
            f"score: {score:.2f}"
        )
    print(f"{'='*60}\n")


def test_category(workers: list[Worker], category: str, expertise: float, budget: tuple[int, int]):
    user_needs = UserNeeds()
    user_needs.user_expertise = expertise
    user_needs.user_price_range = budget

    filtered = filter_by_category(workers, category)
    ranked = rank_workers(filtered, user_needs)
    print_results(ranked, category, user_needs)


async def run(use_db: bool = False):
    if use_db:
        print("Loading workers from MongoDB...")
        workers = await load_workers_from_db()
    else:
        print("Loading workers from JSON...")
        workers = load_workers_from_json("trabajadores.json")

    test_category(workers, category="plomeria",     expertise=4.0, budget=(300, 800))
    test_category(workers, category="electricidad", expertise=5.0, budget=(400, 1200))
    test_category(workers, category="clima",        expertise=3.0, budget=(500, 2000))
    test_category(workers, category="reparaciones", expertise=2.0, budget=(250, 700))
    test_category(workers, category="construccion", expertise=6.0, budget=(500, 3000))
    test_category(workers, category="fumigacion",   expertise=1.0, budget=(300, 1000))
    test_category(workers, category="pintura",      expertise=3.0, budget=(400, 1800))
    test_category(workers, category="limpieza",     expertise=2.0, budget=(300, 900))
    test_category(workers, category="seguridad",    expertise=4.0, budget=(500, 2000))
    test_category(workers, category="computo",      expertise=3.0, budget=(200, 800))
    test_category(workers, category="carpinteria",  expertise=5.0, budget=(400, 1500))


if __name__ == "__main__":
    asyncio.run(run(use_db=True))  # Switch to True to load from MongoDB