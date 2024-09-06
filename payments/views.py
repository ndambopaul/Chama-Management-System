from django.shortcuts import render

# Create your views here.
def upload_nobuk_payments(request):
    return render(request, "payments/chama_payments/upload_payments.html")