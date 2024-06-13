from allocation.domain.model import Batch, OrderLine
from allocation.domain import model
from .unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: str, bactchs: list[Batch]):
    return sku in [batch.sku for batch in bactchs]

def allocate(
        orderid: str,
        sku: str,
        qty: int,
        uow: AbstractUnitOfWork) -> str:
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(sku, batches):
            raise InvalidSku(f"Invalid sku {sku}")
        line = OrderLine(orderid, sku, qty)
        batchref = model.allocate(line, batches)
        uow.commit()
        # b = uow.batches.get(batchref)
    return batchref