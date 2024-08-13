from django.urls import path
from fines.views import chama_fines

urlpatterns = [
    path("", chama_fines, name="fines"),
]
