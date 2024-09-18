from decimal import Decimal
from datetime import datetime, timedelta
import csv
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from users.models import User
from finance.models import MemberSaving, ChamaFine
from savings.models import GroupedSaving, SavingsPayout

# Create your views here.
@login_required(login_url="/users/login/")
def total_savings(request):
    members = GroupedSaving.objects.all().order_by("-created")
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        download_savings = request.POST.get("download_savings")

        print(f"Search Text: {search_text}")
        print(f"Download Savings: {download_savings}")

        if search_text:
            print(f"Search Text: {search_text}")
            members = GroupedSaving.objects.filter(
                Q(member__first_name__icontains=search_text) | Q(member__last_name__icontains=search_text)
            )
        elif download_savings:
            members = GroupedSaving.objects.filter(redeemed=True).order_by("-created")
            response = HttpResponse(content_type="text/csv")
            file_name = f'attachment; filename="Member Savings Report.csv"'
            response["Content-Disposition"] = file_name
            writer = csv.writer(response)
            writer.writerow(
                [
                    "ID",
                    "First Name",
                    "Last Name",
                    "Start Date",
                    "End Date",
                    "Amount Saved",
                ]
            )
            savings_values = members.values_list(
                "id",
                "member__first_name",
                "member__last_name",
                "start_date",
                "end_date",
                "amount_saved",
            )

            for saving in savings_values:
                writer.writerow(saving)

            writer.writerow(["", "", "", "", "", ""])
            return response


    paginator = Paginator(members, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "members": members}
    return render(request, "payments/savings/member_savings.html", context)


@login_required(login_url="/users/login/")
def total_savings_details(request, id):
    grouped_saving = GroupedSaving.objects.get(id=id)
    round_savings = MemberSaving.objects.filter(saving=grouped_saving).order_by("-created")

    paginator = Paginator(round_savings, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "grouped_saving": grouped_saving,
        "page_obj": page_obj
    }
    return render(request, "payments/savings/savings_details.html", context)


@login_required(login_url="/users/login/")
def member_balance_sheet(request):
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
    return render(request, "payments/savings/balance_sheet.html", context)


@login_required(login_url="/users/login/")
def members_savings(request):
    savings = MemberSaving.objects.all().order_by("-created")
    members = User.objects.filter(role="Member").order_by("-created")
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        download_savings = request.POST.get("download_savings")

        if search_text:
            print(f"Search Text: {search_text}")
            savings = MemberSaving.objects.filter(
                Q(member__first_name__icontains=search_text)
                | Q(member__last_name__icontains=search_text)
            )
        elif download_savings:
            savings = MemberSaving.objects.filter(redeemed=False).order_by("-created")
            response = HttpResponse(content_type="text/csv")
            file_name = f'attachment; filename="Member Round Savings Report.csv"'
            response["Content-Disposition"] = file_name
            writer = csv.writer(response)
            writer.writerow(
                [
                    "ID",
                    "First Name",
                    "Last Name",
                    "Merigoround",
                    "Round Date",
                    "Amount Expected",
                    "Amount Saved",
                    "Payment Status",
                ]
            )
            savings_values = savings.values_list(
                "id",
                "member__first_name",
                "member__last_name",
                "merigoround__member__first_name",
                "merigoround__round_date",
                "amount_expected",
                "amount_saved",
                "payment_status",
            )

            for saving in savings_values:
                writer.writerow(saving)

            writer.writerow(["", "", "", "", "", "", "", ""])
            return response

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

        general_savings = GroupedSaving.objects.filter(member=payment.member, active=True, redeemed=False).first()
        if general_savings:
            general_savings.amount_saved += Decimal(amount)
            general_savings.save()
        else:
            GroupedSaving.objects.create(
                member=payment.member,
                start_date=datetime.now().date(),
                end_date=datetime.now().date() + timedelta(days=365),
                amount_saved=Decimal(amount)
            )

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
    
    payment.saving.amount_saved -= payment.amount_saved
    payment.saving.save()
    payment.amount_saved = 0
    payment.save()

    return redirect("members-savings")

@login_required(login_url="/users/login/")
def payout_member_savings(request):
    if request.method == "POST":
        savings_id = request.POST.get("savings_id")
        savings = GroupedSaving.objects.get(id=savings_id)
        savings.redeemed = True
        savings.active = False
        savings.save()

        SavingsPayout.objects.create(
            member=savings.member,
            grouped_saving=savings,
            amount=savings.amount_saved,
            paid=True
        )

        savings_records = MemberSaving.objects.filter(saving=savings)
        savings_records.update(redeemed=True)

        return redirect("savings")
    return render(request, "payments/savings/savings_periods/savings_payout.html")


@login_required(login_url="/users/login/")
def create_savings_period(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        chama_members = User.objects.filter(role="Member")

        for member in chama_members:
            GroupedSaving.objects.create(
                member=member,
                start_date=start_date,
                end_date=end_date
            )
        return redirect("savings")

    return render(request, "payments/savings/savings_periods/create_savings_period.html")


@login_required(login_url="/users/login/")
def savings_payouts(request):
    savings_payouts = SavingsPayout.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        savings_payouts = SavingsPayout.objects.filter(
            Q(member__first_name__icontains=search_text)
            | Q(member__last_name__icontains=search_text)
        )

    paginator = Paginator(savings_payouts, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "payments/savings/savings_payouts.html", context)