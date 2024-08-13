from django.db import models
from core.models import AbstractBaseModel

# Create your models here.
LOAN_STATUS_CHOICES = (
    ("Review", "Review"),
    ("Paid", "Paid"),
    ("Approved", "Approved"),
    ("Declined", "Declined"),
)


class LoanType(AbstractBaseModel):
    name = models.CharField(max_length=255)
    interest_rate = models.DecimalField(max_digits=100, decimal_places=2)
    min_amount = models.DecimalField(max_digits=100, decimal_places=2, default=100)
    max_amount = models.DecimalField(
        max_digits=100, decimal_places=2, default=1000000000
    )
    period = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class Loan(AbstractBaseModel):
    load_type = models.ForeignKey(LoanType, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="memberloans"
    )
    amount_applied = models.DecimalField(max_digits=100, decimal_places=2)
    amount_awarded = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    status = models.CharField(
        max_length=255, choices=LOAN_STATUS_CHOICES, default="Review"
    )
    decline_reason = models.TextField(blank=True, null=True)
    date_due = models.DateField(null=True, blank=True)
    amount_repaid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    amount_to_repay = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name

    @property
    def loan_balance(self):
        return self.amount_to_repay - self.amount_repaid

    @property
    def loan_interest(self):
        return self.amount_to_repay - self.amount_awarded


class LoanPayment(AbstractBaseModel):
    member = models.ForeignKey("users.User", on_delete=models.CASCADE)
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name="loanpayments"
    )
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name
