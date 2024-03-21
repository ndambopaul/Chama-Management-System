from django.shortcuts import render, redirect
from decimal import Decimal
from django.core.paginator import Paginator
from users.models import User
from loans.models import Loan, LoanPayment
# Create your views here.
def loans(request):
    loans = Loan.objects.all()

    members = User.objects.filter(role="Member")
    paginator = Paginator(loans, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "members": members
    }

    return render(request, "loans/loans.html", context)

def new_loan(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        amount_applied = request.POST.get('amount_applied')
        date_due = request.POST.get('date_due')

        amount = Decimal(amount_applied)
        repay_amount = amount + (amount * Decimal(0.16))

        Loan.objects.create(
            member_id=member_id,
            amount_applied=amount,
            date_due=date_due,
            status="Review",
            amount_to_repay=repay_amount
        )

        return redirect("loans")

    return render(request, "loans/new_loan.html")


def edit_loan(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        amount_awarded = request.POST.get('amount_awarded')
        amount_applied = request.POST.get('amount_applied')

        awarded_amount = Decimal(amount_awarded) 
        applied_amount = Decimal(amount_applied)


        loan = Loan.objects.get(id=loan_id)
        loan.amount_awarded = awarded_amount
        loan.amount_applied = applied_amount
        loan.save()

        return redirect("loans")    

    return render(request, "loans/edit_loan.html")


def approve_loan(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        loan = Loan.objects.get(id=loan_id)
        loan.status = "Approved"
        loan.amount_awarded = loan.amount_applied
        loan.amount_to_repay = loan.amount_awarded + (loan.amount_awarded * Decimal(0.16))
        loan.save()
        return redirect("loans")
    
    return render(request, "loans/approve_loan.html")


def decline_loan(request):
    if request.method == "POST":
        loan_id = request.POST.get("loan_id")
        decline_reason = request.POST.get("decline_reason")
        loan = Loan.objects.get(id=loan_id)
        loan.status = "Declined"
        loan.decline_reason = decline_reason
        loan.save()

        return redirect("loans")
    return render(request, "loans/decline_loan.html")

#### LOANS PAYMENTS

def loan_payments(request):
    loan_payments = LoanPayment.objects.all()

    paginator = Paginator(loan_payments, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }

    return render(request, "payments/loan_payments/loan_payments.html", context)


def new_loan_payment(request):
    if request.method == "POST":
        member_id = request.POST.get('member_id')
        loan_id = request.POST.get('loan_id')
        amount_paid = request.POST.get('amount_paid')

        amount = Decimal(amount_paid)
        loan = Loan.objects.get(id=loan_id)

        LoanPayment.objects.create(member_id=member_id, loan_id=loan_id, amount=amount)
        loan.amount_repaid += amount
        loan.save()

        if loan.amount_repaid == loan.amount_to_repay:
            loan.status = "Paid"
            loan.save()
       

        return redirect('loan-payments')

    return render(request, "payments/loan_payments/pay_loan.html")