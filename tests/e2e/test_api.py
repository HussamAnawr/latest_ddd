import pytest
from allocation.adapters.repository import DjangoRepository
from allocation.domain import model
from ninja.testing import TestClient
from djangoproject.django_project.api import router

@pytest.fixture
def add_stock():
    
    def _add_stock(lines):
        for ref, sku, qty, eta in lines:
            DjangoRepository().add(model.Batch(ref, sku, qty, eta))
    
    yield _add_stock

@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock):
    add_stock([
        ("111", "TABUL-BLUE", 30, "2011-01-02"),
        ("123", "TABUL-BLUE", 100, "2011-01-01"),
        ("122", "TABUL-RED", 100, None),
    ])

    client = TestClient(router)
    r = client.post("allocate", json={"orderid": "order123", "sku": "TABUL-BLUE", "qty": 3})

    assert r.status_code == 200
    assert len(DjangoRepository().list()) == 3
    assert r.json()['batchref'] == "123"
    assert DjangoRepository().get("123").available_quantity == 97



@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures("restart_api")
def test_allocations_are_persisted(add_stock):
    add_stock([
        ("111", "TABUL-BLUE", 30, "2011-01-02"),
        ("123", "TABUL-BLUE", 30, "2011-01-01"),
        ("122", "TABUL-RED", 100, None),
    ])
    client = TestClient(router)
    r = client.post("allocate", json={"orderid": "order123", "sku": "TABUL-BLUE", "qty": 25})



    assert r.status_code == 200
    assert len(DjangoRepository().list()) == 3
    assert r.json()['batchref'] == "123"

    r = client.post("allocate", json={"orderid": "order123", "sku": "TABUL-BLUE", "qty": 25})

    assert r.json()['batchref'] == "111"