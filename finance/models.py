from django.db import models
from core.models import AbstractBaseModel

# Create your models here.
ROUND_CHOICES = (
    ("5th", "Round ya 5th"),
    ("17th", "Round ya 17th"),
)

PAYMENT_STATUS = (
    ("Pending", "Pending"),
    ("Paid", "Paid"),
    ("Defaulted", "Defaulted"),
    ("Cancelled", "Cancelled"),
)


class MeriGoRound(AbstractBaseModel):
    member = models.ForeignKey("users.User", on_delete=models.CASCADE)
    round_date = models.DateField()
    amount_expected = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    amount_raised = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name
    
    @property
    def chama_round(self):
        return f"{self.round_date.day}th"


class MemberSaving(AbstractBaseModel):
    merigoround = models.ForeignKey(MeriGoRound, on_delete=models.CASCADE, null=True)
    member = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="membersavings")
    amount_expected = models.DecimalField(max_digits=100, decimal_places=2, default=250)
    amount_saved = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    savings_round = models.CharField(max_length=255, choices=ROUND_CHOICES)
    paid = models.BooleanField(default=False)
    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STATUS, default="Pending"
    )
    amount_fined = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name


class MeriGoRoundPayment(AbstractBaseModel):
    merigoround = models.ForeignKey(MeriGoRound, on_delete=models.CASCADE, null=True)
    member = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="membermpayments")
    amount_expected = models.DecimalField(max_digits=100, decimal_places=2, default=1500)
    amount_paid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    chama_round = models.CharField(max_length=255, choices=ROUND_CHOICES)
    paid = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, default="Pending")

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name


class Payment(AbstractBaseModel):
    member = models.ForeignKey("users.User", on_delete=models.CASCADE)
    merigoround = models.ForeignKey(MeriGoRound, on_delete=models.CASCADE, null=True)
    chama_amount = models.DecimalField(max_digits=100, decimal_places=2, default=1500)
    savings_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    amount_fined = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    closed = models.BooleanField(default=False)


    def __str__(self):
        return self.member.first_name + " " + self.member.last_name


class ChamaFine(AbstractBaseModel):
    member = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="memberfines")
    merigoround = models.ForeignKey(MeriGoRound, on_delete=models.CASCADE, null=True)
    amount_fined = models.DecimalField(max_digits=100, decimal_places=2, default=100)

    def __str__(self):
        return self.member.first_name + " " + self.member.last_name