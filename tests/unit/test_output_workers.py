from functions.weight_functions import output_workers
from classes.weight_classes import Worker


def create_worker(
    worker_id,
    rating,
    reviews
):
    return Worker(
        id=worker_id,
        nombre=f"Worker {worker_id}",
        categorias=["plomeria"],
        calificacion_global=rating,
        insignias=[],
        disponible=True,
        precio_desde=100,
        precio_hasta=200,
        total_reviews=reviews
    )

def test_output_workers_returns_top_three():
    workers = [
        create_worker("1", 5.0, 100),
        create_worker("2", 4.5, 90),
        create_worker("3", 4.0, 80),
        create_worker("4", 3.5, 70),
    ]

    result = output_workers(
        workers,
        category="plomeria",
        expertise=1.0,
        budget=(100, 500)
    )

    assert len(result) == 3

def test_output_workers_sorted():
    workers = [
        create_worker("bad", 3.0, 10),
        create_worker("good", 5.0, 150),
    ]

    result = output_workers(
        workers,
        category="plomeria",
        expertise=1.0,
        budget=(100, 500)
    )

    assert result[0][0] == "good"