from allocation.adapters.repository import DjangoRepository
from allocation.domain import model 
from djangoproject.alloc import models as django_models
from django.db import connection
import pytest
from datetime import date


def insert_raw_sql_batch(batch: model.Batch):
    with connection.cursor() as cursor:
        cursor.execute(f'INSERT INTO alloc_batch (reference, sku, qty, eta) VALUES (%s, %s, %s, %s)',
                       [batch.reference, batch.sku, batch._purchased_quantity, batch.eta])

def insert_raw_sql_order_line(line: model.OrderLine):
    with connection.cursor() as cursor:
        cursor.execute(f'INSERT INTO alloc_orderline (orderid, sku, qty) VALUES (%s, %s, %s)',
                       [line.orderid, line.sku, line.qty])



@pytest.mark.django_db
def test_repository_can_save_a_batch():
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=date(2011, 12, 25))
    repo = DjangoRepository()
    repo.add(batch)
    
    # transaction.commit()
    [saved_batch] = django_models.Batch.objects.all()
    assert saved_batch.reference == batch.reference
    assert saved_batch.sku == batch.sku
    assert saved_batch.qty == batch._purchased_quantity
    assert saved_batch.eta == batch.eta
    assert django_models.Batch.objects.all().count() == 1


@pytest.mark.django_db
def test_cheack_batch():
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=date(2011, 12, 25))
    line = model.OrderLine("order123", "RUSTY-SOAPDISH", 10)
    insert_raw_sql_batch(batch)
    insert_raw_sql_order_line(line)
    repo = DjangoRepository()
    b = repo.get("batch1")
    
    # transaction.commit()
    assert b.sku == "RUSTY-SOAPDISH"

@pytest.mark.django_db
def test_batch_with_allocate():
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=date(2011, 12, 25))
    line1 = model.OrderLine("order123", "RUSTY-SOAPDISH", 10)
    line2 = model.OrderLine("order124", "RUSTY-SOAPDISH", 12)
    model.allocate(line1, [batch])
    model.allocate(line2, [batch])
    repo = DjangoRepository()
    repo.add(batch)
    retrived_batch = repo.get("batch1")
    assert django_models.OrderLine.objects.all().count() == 2
    assert django_models.Allocation.objects.all().count() == 2
    assert retrived_batch.available_quantity == 78
    assert model.OrderLine("order123", "RUSTY-SOAPDISH", 10) in retrived_batch._allocations
    assert model.OrderLine("order124", "RUSTY-SOAPDISH", 12) in retrived_batch._allocations

