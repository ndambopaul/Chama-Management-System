from django.db import models
from core.models import AbstractBaseModel
# Create your models here.
LOAN_STATUS_CHOICES = (
    ("Review", "Review"),
    ("Paid", "Paid"),
    ("Approved", "Approved"),
    ("Declined", "Declined"),
)

class Loan(AbstractBaseModel):
    member = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    amount_applied = models.DecimalField(max_digits=100, decimal_places=2)
    amount_awarded = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    status = models.CharField(max_length=255, choices=LOAN_STATUS_CHOICES, default="Review")
    decline_reason = models.TextField(blank=True, null=True)
    date_due = models.DateField(null=True, blank=True)
    amount_repaid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    amount_to_repay = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name
    

    @property
    def loan_balance(self):
        return self.amount_to_repay - self.amount_repaid


class LoanPayment(AbstractBaseModel):
    member = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name
