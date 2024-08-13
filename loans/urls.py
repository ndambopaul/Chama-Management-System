from django.urls import path
from loans.views import (
    loans,
    home,
    loan_payments,
    edit_loan,
    loan_details,
    new_loan_payment,
    new_loan,
    approve_loan,
    decline_loan,
)

urlpatterns = [
    path("", loans, name="loans"),
    path("loans-home/", home, name="loans-home"),
    path("<int:id>/", loan_details, name="loan-details"),
    path("new-loan/", new_loan, name="new-loan"),
    path("approve-loan/", approve_loan, name="approve-loan"),
    path("decline-loan/", decline_loan, name="decline-loan"),
    path("loan-payments", loan_payments, name="loan-payments"),
    path("pay-loan/", new_loan_payment, name="pay-loan"),
]
