from classes.weight_classes import Worker
from classes.chat_classes import UserNeeds, PriceRange


def create_worker():
    return Worker(
        id="1",
        nombre="Juan",
        categorias=["plomeria"],
        calificacion_global=5.0,
        insignias=["Top"],
        disponible=True,
        precio_desde=100,
        precio_hasta=200,
        total_reviews=120
    )


def create_user_needs():
    return UserNeeds(
        user_expected_expertise=1.0,
        user_price_range=PriceRange(
            min=100,
            max=300
        ),
        category="plomeria"
    )

from functions.weight_functions import calculate_worker_score


def test_worker_score_positive():
    score = calculate_worker_score(
        create_worker(),
        create_user_needs()
    )

    assert score > 0

def test_better_rating_gets_higher_score():
    worker1 = create_worker()
    worker2 = create_worker()

    worker2.global_rating = 3.0

    needs = create_user_needs()

    score1 = calculate_worker_score(worker1, needs)
    score2 = calculate_worker_score(worker2, needs)

    assert score1 > score2