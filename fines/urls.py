from django.urls import path
from fines.views import chama_fines, dispute_fine, resolve_disputed_fine

urlpatterns = [
    path("", chama_fines, name="fines"),
    path("dispute-fine/", dispute_fine, name="dispute-fine"),
    path("resolve-fine-dispute/", resolve_disputed_fine, name="resolve-fine-dispute"),
]
