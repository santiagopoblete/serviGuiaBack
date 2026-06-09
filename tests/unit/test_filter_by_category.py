from functions.weight_functions import filter_by_category
from classes.weight_classes import Worker


def create_worker(worker_id, categories):
    return Worker(
        id=worker_id,
        nombre="Test",
        categorias=categories,
        calificacion_global=5.0,
        insignias=[],
        disponible=True,
        precio_desde=100,
        precio_hasta=200,
        total_reviews=50
    )


def test_filter_exact_category():
    workers = [
        create_worker("1", ["plomeria"]),
        create_worker("2", ["electricidad"])
    ]

    result = filter_by_category(workers, "plomeria")

    assert len(result) == 1
    assert result[0].id == "1"


def test_filter_subcategory():
    workers = [
        create_worker("1", ["plomeria.fugas"]),
        create_worker("2", ["electricidad"])
    ]

    result = filter_by_category(workers, "plomeria")

    assert len(result) == 1
    assert result[0].id == "1"