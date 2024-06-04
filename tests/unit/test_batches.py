from allocation.domain.model import Batch, OrderLine
from datetime import date
import pytest

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )

def test_allocating_to_a_batch_reduce_available_quantity():
    batch = Batch("batch-001", "SMALL_TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL_TABLE", 2)
    batch.allocate(line)
    assert batch.available_quantity == 18

@pytest.mark.parametrize(['batch_qty', 'line_qty', 'expected'],[
    (20, 2, True), # batch.qty > line.qty
    (2, 20, False),  # batch.qty < line.qty
    (2, 2, True),  # batch.qty == line.qty

])
def test_can_allocate_(batch_qty, line_qty, expected):
    batch, line = make_batch_and_line("BLUE_TABLE", batch_qty, line_qty)
    assert batch.can_allocate(line) is expected

def test_can_allocate_if_skus_do_not_match():
    batch = Batch("batch001", "BLUE_SMALL_TABLE", 100, eta=date.today())
    line = OrderLine("order-123", "SMALL_TABLE", 10)
    assert batch.can_allocate(line) is False