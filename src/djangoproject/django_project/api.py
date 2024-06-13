from ninja import NinjaAPI, Schema
from ninja import Router
from allocation.service_layer import services
from allocation.service_layer.unit_of_work import DjangoUintOfWork
from allocation.domain.model import OutOfStock

import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = "djangoproject.django_project.settings"
django.setup()


api =  NinjaAPI()
router = Router()

class AllocateIn(Schema):
    orderid: str
    sku: str
    qty: int

@router.post("allocate")
def allocate(request, data: AllocateIn):
    try:
        batchref = services.allocate(data.orderid, data.sku, data.qty, DjangoUintOfWork())
    except (OutOfStock, services.InvalidSku) as e:
        return {"message": (str(e))}
    
    return {"batchref": batchref}

api.add_router("", router)