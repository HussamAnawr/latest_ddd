from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: str

class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.ref = ref
        self.sku = sku
        self._purchased_quantity = qty
        self.eta = eta
        self._allocations = set()
    
    def allocate(self, line: OrderLine) -> None:
        self.available_quantity -= line.qty
    
    @property
    def allcoated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
