from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from finance.models import ChamaFine


# Create your views here.
@login_required(login_url="/users/login/")
def chama_fines(request):
    chama_fines = ChamaFine.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        chama_fines = ChamaFine.objects.filter(
            Q(member__first_name__icontains=search_text)
            | Q(member__last_name__icontains=search_text)
            | Q(member__id_number__icontains=search_text)
        )

    paginator = Paginator(chama_fines, 13)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "fines/fines.html", context)
