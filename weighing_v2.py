import random
from classes import Worker

class UserNeeds:
    user_expertise: float = 0.0
    user_price_range: tuple[int, int] = (0, 0)


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

    # Combine scores
    score += expertise_score / 10.0 - user_needs.user_expertise
    score = max(score, 0.0)
    score += pricing_score
    score = min(score, 10.0)

    return score


# Example usage
user_needs = UserNeeds()
user_needs.user_expertise = 4.0
user_needs.user_price_range = (800, 1000)

workers = []
workers_scores = []

for i in range(25):
    worker = Worker(
        id=f"t{i+1:03}",
        name=f"Worker {i+1}",
        categories=["electricidad"],
        global_rating=round(random.uniform(0.0, 5.0), 2),
        badges=random.sample(
            ["top_experience", "always_on_time", "certified", "formal_worker"],
            k=random.randint(0, 3)
        ),
        available=True,
        price_from=random.randint(400, 1250),
        price_to=random.randint(650, 2500),
        total_reviews=random.randint(0, 150),
    )
    workers.append(worker)
    workers_scores.append(calculate_worker_score(worker, user_needs))

workers_with_scores = list(zip(workers, workers_scores))
workers_with_scores.sort(key=lambda x: x[1], reverse=True)

for i, (worker, score) in enumerate(workers_with_scores):
    print(
        f"#{i+1} {worker.name} | "
        f"rating: {worker.global_rating} ({worker.total_reviews} reviews) | "
        f"badges: {len(worker.badges)} | "
        f"price: {worker.price_from}-{worker.price_to} | "
        f"score: {score:.2f}"
    )