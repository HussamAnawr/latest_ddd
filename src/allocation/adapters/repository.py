import abc
from allocation.domain import model
from djangoproject.alloc import models as django_model

class AbstractRepository(abc.ABC):
    def __init__(self) -> None:
        self.seen = set() ## to be used


    def add(self, batch: model.Batch):
        self.seen.add(batch)
    
    def get(self, reference) -> model.Batch:
        batch = self._get(reference)
        if batch:
            self.seen.add(batch)
        return batch
    
    @abc.abstractmethod
    def _get(self, reference) -> model.Batch:
        raise NotImplementedError
    
class DjangoRepository(AbstractRepository):
    def add(self, batch: model.Batch):
        super().add(batch)
        self.update(batch)

    def _get(self, reference):
        return django_model.Batch.objects.filter(reference=reference).first().to_domain()
    
    def list(self):
        batches = [b.to_domain() for b in django_model.Batch.objects.all()]
        self.seen = self.seen.union(set(batches))
        return batches
    
    def update(self, batch: model.Batch):
         django_model.Batch.update_from_domain(batch)