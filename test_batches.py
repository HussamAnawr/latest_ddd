from model import Batch, OrderLine
from datetime import date
def test_allocating_to_a_batch_reduce_available_quantity():
    batch = Batch("batch-001", "SMALL_TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL_TABLE", 2)
    batch.allocate(line)
    assert batch.available_quantity == 18