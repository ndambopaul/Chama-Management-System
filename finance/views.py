from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from finance.models import Payment, MemberSaving, MeriGoRound, MeriGoRoundPayment, ChamaFine
from users.models import User
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from decimal import Decimal
# Create your views here.
## PAYMENTS COLLECTIONS
@login_required(login_url="/users/login/")
def payments(request):
    payments = Payment.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        payments = Payment.objects.filter(Q(member__first_name__icontains=search_text) | Q(member__last_name__icontains=search_text))

    paginator = Paginator(payments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "payments/payments.html", context)

@login_required(login_url="/users/login/")
def new_payment(request):
    return render(request, "payments/new_payment.html")


## MERI GO ROUNDS
@login_required(login_url="/users/login/")
def chama_rounds(request):
    chama_rounds = MeriGoRound.objects.all().order_by("-created")

    members = User.objects.filter(role="Member")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        chama_rounds = MeriGoRound.objects.filter(Q(member__first_name__icontains=search_text) | Q(member__last_name__icontains=search_text))


    paginator = Paginator(chama_rounds, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "members": members}
    return render(request, "chama_rounds/chama_rounds.html", context)

@login_required(login_url="/users/login/")
def end_chama_round(request,chama_round_id):
    chama_round = MeriGoRound.objects.get(id=chama_round_id)
    chama_round.done = True
    chama_round.save()
    return redirect('chama-rounds')

@login_required(login_url="/users/login/")
def delete_chama_round(request):
    if request.method == 'POST':
        chama_round_id = request.POST.get('chama_round_id')

        chama_round = MeriGoRound.objects.get(id=chama_round_id)
        chama_round.delete()

        return redirect('chama-rounds')
    return render(request, 'chama_rounds/delete_chama_round.html')

#@login_required(login_url="/users/login/")
@transaction.atomic
def new_chama_round(request):
    if request.method == "POST":
        member = request.POST.get("member")
        round_date = request.POST.get("round_date")
        chama_round_type = request.POST.get("chama_round")

        try:
            members_count = User.objects.filter(role="Member").count()
            member = User.objects.get(id=member)

            chama_round = MeriGoRound.objects.create(
                member=member,
                round_date=round_date,
                amount_expected=members_count * 1500,
                amount_raised=0,
            )
            # Create Chama Payment Records
            chama_payments_list = []
            members = User.objects.filter(role="Member")

            for member in members:
                chama_payments_list.append(
                    MeriGoRoundPayment(
                        merigoround=chama_round,
                        member=member,
                        amount_expected=1500,
                        amount_paid=0,
                        chama_round=chama_round_type,
                        paid=False,
                    )
                )
            MeriGoRoundPayment.objects.bulk_create(chama_payments_list)

            members_savings_list = []
            for member in members:
                members_savings_list.append(
                    MemberSaving(
                        merigoround=chama_round,
                        member=member,
                        amount_expected=250,
                        amount_saved=0,
                        savings_round=chama_round_type,
                        paid=False,
                    )
                )
            MemberSaving.objects.bulk_create(members_savings_list)
            
            # Create Member Savings Records
            print(f"Member: {member}, Round Date: {round_date}")
            return redirect("chama-rounds")
        except Exception as e:
            raise e
    return render(request, "chama_rounds/new_chama_round.html")


## MEMBER SAVINGS
@login_required(login_url="/users/login/")
def total_savings(request):
    members = User.objects.filter(role="Member").order_by("-created")
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        members = User.objects.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text))

    paginator = Paginator(members, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "members": members
    }
    return render(request, "payments/savings/member_savings.html", context)

@login_required(login_url="/users/login/")
def members_savings(request):
    savings = MemberSaving.objects.all().order_by("-created")
    members = User.objects.filter(role="Member").order_by("-created")
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        savings = MemberSaving.objects.filter(Q(member__first_name__icontains=search_text) | Q(member__last_name__icontains=search_text))

    paginator = Paginator(savings, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "members": members
    }
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
                amount_fined=Decimal(fine)
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


# MERI GO ROUND PAYMENTS
@login_required(login_url="/users/login/")
def chama_round_payments(request):
    chama_round_payments = MeriGoRoundPayment.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        chama_round_payments = MeriGoRoundPayment.objects.filter(Q(member__first_name__icontains=search_text) | Q(member__last_name__icontains=search_text))


    paginator = Paginator(chama_round_payments, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "payments/chama_payments/round_payments.html", context)


@login_required(login_url="/users/login/")
def mark_chama_payments_as_paid(request, payment_id):
    payment = MeriGoRoundPayment.objects.get(id=payment_id)
    payment.paid = True
    payment.payment_status = "Paid"
    payment.amount_paid = 1500
    payment.save()
    payment.merigoround.amount_raised += 1500
    payment.merigoround.save()

    print(payment.merigoround.amount_raised)
    

    return redirect("chama-payments")

@login_required(login_url="/users/login/")
def mark_chama_payments_as_defaulted(request, payment_id):
    payment = MeriGoRoundPayment.objects.get(id=payment_id)
    payment.paid = False
    payment.payment_status = "Defaulted"
    payment.amount_paid = 0
    payment.save()

    return redirect("chama-payments")

@login_required(login_url="/users/login/")
def mark_chama_payments_as_reset(request, payment_id):
    payment = MeriGoRoundPayment.objects.get(id=payment_id)
    if payment.payment_status == "Paid":
        payment.merigoround.amount_raised -= payment.amount_paid
        payment.merigoround.save()
    payment.paid = False
    payment.payment_status = "Pending"
    payment.amount_paid = 0
    payment.save()

    return redirect("chama-payments")

@login_required(login_url="/users/login/")
def mark_chama_payments_as_cancelled(request, payment_id):
    payment = MeriGoRoundPayment.objects.get(id=payment_id)
    if payment.payment_status == "Paid":
        payment.merigoround.amount_raised -= payment.amount_paid
        payment.merigoround.save()
    payment.paid = False
    payment.payment_status = "Cancelled"
    payment.amount_paid = 0
    payment.save()

    return redirect("chama-payments")


## FINES
@login_required(login_url="/users/login/")
def chama_fines(request):
    chama_fines = ChamaFine.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        print(f"Search Text: {search_text}")
        chama_fines = ChamaFine.objects.filter(Q(member__first_name__icontains=search_text) | Q(member__last_name__icontains=search_text))


    paginator = Paginator(chama_fines, 13)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }

    return render(request, "payments/chama_fines.html", context)