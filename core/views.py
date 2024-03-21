from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import User
# Create your views here.
@login_required(login_url="/users/login")
def home(request):
    members = User.objects.filter(role="Member").count()

    context = {
        "members_count": members
    }
    return render(request, "home.html", context)
