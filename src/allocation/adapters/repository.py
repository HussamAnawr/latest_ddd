import abc
from allocation.domain import model
from djangoproject.alloc import models as django_model

class AbstractRepository(abc.ABC):
    def __init__(self) -> None:
        self.seen = set() ## to be used

    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
    
class DjangoRepository(AbstractRepository):
    def add(self, batch: model.Batch):
        django_model.Batch.update_from_domain(batch)

    def get(self, reference):
        return django_model.Batch.objects.filter(reference=reference).first().to_domain()
    
    def list(self):
        return [b.to_domain() for b in django_model.Batch.objects.all()]