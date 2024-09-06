from django.urls import path
from payments.views import upload_nobuk_payments

urlpatterns = [
    path("upload-nobuk-payments/", upload_nobuk_payments, name="upload-nobuk-payments"),
]