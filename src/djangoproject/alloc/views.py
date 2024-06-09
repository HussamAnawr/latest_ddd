from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from allocation.domain import model
import json
from datetime import datetime
import os
import django
from allocation.adapters.repository import DjangoRepository

os.environ["DJANGO_SETTINGS_MODULE"] = "djangoproject.django_project.settings"
django.setup()

# @csrf_exempt
# def allocate(request):
#     data = json.load(request.body)
#     # eta = data['eta']
#     # if eta is not None:
#     #     eta = datetime.fromisoformat(data).date()
#     batches = DjangoRepository.list()
#     line = model.OrderLine(data['orderid'], data['sku'], data['qty'])
#     batchref = model.allocate(line, batches)
#     return {"batchref": batchref}, 201

# @csrf_exempt
# def add_batch(request):
#     data = json.load(request.body)
#     batch = 