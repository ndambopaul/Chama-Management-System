from django.db import models
from core.models import AbstractBaseModel
from django.contrib.auth.models import AbstractUser
from finance.models import MemberSaving, MeriGoRoundPayment, ChamaFine
from loans.models import Loan, LoanPayment

# Create your models here.
USER_ROLES = (
    ("admin", "Admin"),
    ("member", "Member"),
)


class User(AbstractUser, AbstractBaseModel):
    role = models.CharField(max_length=255, choices=USER_ROLES)
    id_number = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True)
    county = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    round_number = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_savings(self):
        return sum(self.membersavings.all().values_list("amount_saved", flat=True))
    
    @property
    def total_fines(self):
        return sum(self.memberfines.all().values_list("amount_fined", flat=True))
    
    @property
    def total_loans(self):
        return sum(self.memberloans.all().values_list("amount_awarded", flat=True))
