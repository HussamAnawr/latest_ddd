from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

class OutOfStock(Exception):
    pass

def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.referance
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: str

class Batch:

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.referance = ref
        self.sku = sku
        self._purchased_quantity = qty
        self.eta = eta
        self._allocations = set()
    
    def __hash__(self) -> int:
        return hash(self.referance)
    
    def __repr__(self) -> str:
        return f"<Batch {self.referance}>"
    
    def __eq__(self, other: Batch) -> bool:
        if not isinstance(other, Batch):
            return False
        return self.referance == other.referance

    def __gt__(self, other: Batch):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta 
    
    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)
    

    @property
    def allcoated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allcoated_quantity
    
    def can_allocate(self, line: OrderLine) -> bool:
        return line.sku == self.sku and self.available_quantity >= line.qty