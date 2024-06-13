from allocation.domain.model import Batch, OrderLine
from allocation.domain import model
from allocation.adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: str, bactchs: list[Batch]):
    return sku in [batch.sku for batch in bactchs]

def allocate(
        orderid: str,
        sku: str,
        qty: int,
        repo: AbstractRepository) -> str:
    batches = repo.list()
    if not is_valid_sku(sku, batches):
        raise InvalidSku(f"Invalid sku {sku}")
    line = OrderLine(orderid, sku, qty)
    batchref = model.allocate(line, batches)
    return batchref