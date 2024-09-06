from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from finance.models import ChamaFine, MemberSaving


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


@login_required(login_url="/users/login/")
def dispute_fine(request):
    if request.method == "POST":
        fine_id = request.POST.get("fine")
        fine = ChamaFine.objects.get(id=fine_id)
        fine.status = "Disputed"
        fine.save()
        return redirect("fines")
    return render(request, "fines/dispute_fine.html")


@login_required(login_url="/users/login/")
def resolve_disputed_fine(request):
    if request.method == "POST":
        fine_id = request.POST.get("fine")
        decision = request.POST.get("decision")

        fine = ChamaFine.objects.get(id=fine_id)
        if decision == "Settled":
            fine.status = "Settled"
            fine.save()

        elif decision == "Refunded":
            fine.status = "Refunded"

            savings_round = MemberSaving.objects.get(
                member=fine.member,
                merigoround=fine.merigoround
            )
            savings_round.amount_saved += fine.amount_fined
            savings_round.save()

            savings_round.saving.amount_saved += fine.amount_fined
            savings_round.saving.save()
            fine.amount_fined = 0
            fine.save()
            
        return redirect("fines")
    return render(request, "fines/resolve_fine_dispute.html")
