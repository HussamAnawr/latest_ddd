from django.db import models
from allocation.domain import model as domain_model
# Create your models here.

class Batch(models.Model):
    reference = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    eta = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"<BATCH({self.id}) reference:{self.reference} sku:{self.sku} qty:{self.qty} eta:{self.eta}>"
    

    @staticmethod
    def update_from_domain(batch: domain_model.Batch):
        try:
            b = Batch.objects.get(reference=batch.reference)
        except Batch.DoesNotExist:
            b = Batch(reference=batch.reference)
        b.sku = batch.sku
        b.qty = batch._purchased_quantity
        b.eta = batch.eta
        b.save()
        b.allocations.set(
            Allocation.from_domain(l, b) for l in batch._allocations
        )
    
    def to_domain(self) -> domain_model.Batch:
        b = domain_model.Batch(ref=self.reference, sku=self.sku, qty=self.qty, eta=self.eta)
        b._allocations = set(
            a.line.to_domain() for a in self.allocations.all()
        )
        return b



class OrderLine(models.Model):
    orderid = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    
    def __str__(self) -> str:
        return f"<ORDER_LINE orderid:{self.orderid} sku:{self.sku} qty:{self.qty}>"
    
    def to_domain(self):
        return domain_model.OrderLine(orderid=self.orderid, sku=self.sku, qty=self.qty)

    @staticmethod
    def from_domain(line: domain_model.OrderLine):
        l, _ = OrderLine.objects.get_or_create(
            orderid=line.orderid, sku=line.sku, qty = line.qty
        )
        return l


class Allocation(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="allocations")
    line = models.ForeignKey(OrderLine, on_delete=models.CASCADE,)

    def __str__(self) -> str:
        return f"batch: {self.batch}, line: {self.line}"

    @staticmethod
    def from_domain(domain_line: domain_model.OrderLine, django_batch: Batch):
        a, _ = Allocation.objects.get_or_create(
            line=OrderLine.from_domain(domain_line),
            batch=django_batch
        )
        return a
