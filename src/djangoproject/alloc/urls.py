from alloc import views
from django.urls import path

urlpatterns = [
    path('allocate', views.allocate),
]