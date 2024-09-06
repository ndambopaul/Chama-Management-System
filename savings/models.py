from django.db import models

from core.models import AbstractBaseModel
# Create your models here.
class GroupedSaving(AbstractBaseModel):
    member = models.ForeignKey("users.User", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount_saved = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    redeemed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member.username} {self.start_date} - {self.end_date} Savings"