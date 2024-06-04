from datetime import date, timedelta
from allocation.domain.model import Batch, OrderLine, allocate, OutOfStock
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def test_prefers_current_stock_batch_to_shipments():
    in_stock_batch = Batch('in-stock-123', "RETRO_CLOCK", 100, eta=None)
    shipment_batch = Batch('shipment-batch-123', "RETRO_CLOCK", 100, eta=tomorrow)
    line = OrderLine('order-123', "RETRO_CLOCK", 10)
    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch('speedy-123', "MIMI-SPOON", 100, eta=today)
    medium = Batch('normal-123', "MIMI-SPOON", 100, eta=tomorrow)
    latest = Batch('slow-123', "MIMI-SPOON", 100, eta=later)
    line = OrderLine('order-123', "MIMI-SPOON", 10)
    allocate(line, [medium, latest, earliest])
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

def test_retuen_allocated_batch_ref():
    in_stock_batch = Batch('in-stock-123', "RETRO_CLOCK", 100, eta=None)
    shipment_batch = Batch('shipment-batch-123', "RETRO_CLOCK", 100, eta=tomorrow)
    line = OrderLine('order-123', "RETRO_CLOCK", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation ==  in_stock_batch.referance

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', "SMALL-FORK", 10, eta=today)
    allocate(OrderLine('order123', 'SMALL-FORK', 10), [batch])
    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine('order13', 'SMALL-FORK', 1), [batch])