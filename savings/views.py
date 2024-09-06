from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from users.models import User
from finance.models import MemberSaving, GroupedSaving, ChamaFine


# Create your views here.
@login_required(login_url="/users/login/")
def total_savings(request):
    members = User.objects.filter(role="Member").order_by("-created")
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        members = User.objects.filter(
            Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text)
        )

    paginator = Paginator(members, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "members": members}
    return render(request, "payments/savings/member_savings.html", context)


@login_required(login_url="/users/login/")
def members_savings(request):
    savings = MemberSaving.objects.all().order_by("-created")
    members = User.objects.filter(role="Member").order_by("-created")
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        savings = MemberSaving.objects.filter(
            Q(member__first_name__icontains=search_text)
            | Q(member__last_name__icontains=search_text)
        )

    paginator = Paginator(savings, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "members": members}
    return render(request, "payments/savings/savings.html", context)


@login_required(login_url="/users/login/")
def mark_member_savings_as_paid(request):
    if request.method == "POST":
        savings_id = request.POST.get("savings_id")
        amount = request.POST.get("amount")
        fine = request.POST.get("fine")

        payment = MemberSaving.objects.get(id=savings_id)
        payment.paid = True
        payment.payment_status = "Paid"
        payment.amount_saved = Decimal(amount)
        payment.save()

        print(f"Fine Amount: {type(fine)}")

        if fine not in [0, "0"]:
            payment.amount_fined = Decimal(fine)
            payment.save()

            ChamaFine.objects.create(
                member=payment.member,
                merigoround=payment.merigoround,
                amount_fined=Decimal(fine),
            )

    return redirect("members-savings")


@login_required(login_url="/users/login/")
def mark_member_savings_as_defaulted(request, savings_id):
    payment = MemberSaving.objects.get(id=savings_id)
    payment.paid = False
    payment.payment_status = "Defaulted"
    payment.amount_saved = 0
    payment.save()

    return redirect("members-savings")


@login_required(login_url="/users/login/")
def mark_member_savings_as_reset(request, savings_id):
    payment = MemberSaving.objects.get(id=savings_id)
    payment.paid = False
    payment.payment_status = "Pending"
    payment.amount_saved = 0
    payment.save()

    return redirect("members-savings")


@login_required(login_url="/users/login/")
def mark_member_savings_as_cancelled(request, savings_id):
    payment = MemberSaving.objects.get(id=savings_id)
    payment.paid = False
    payment.payment_status = "Cancelled"
    payment.amount_saved = 0
    payment.save()

    return redirect("members-savings")