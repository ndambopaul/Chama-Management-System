from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User
from loans.models import Loan
# Create your views here.
@login_required(login_url="/users/login")
def home(request):
    members = User.objects.filter(role="Member").count()

    loans_amount = sum(list(Loan.objects.filter(status="Approved").values_list("amount_awarded", flat=True)))


    context = {
        "members_count": members,
        "loans_amount": loans_amount
    }
    return render(request, "home.html", context)
