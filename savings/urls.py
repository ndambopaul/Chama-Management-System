from django.urls import path
from savings.views import (
    members_savings,
    total_savings_details,
    mark_member_savings_as_cancelled,
    mark_member_savings_as_paid,
    mark_member_savings_as_reset,
    mark_member_savings_as_defaulted,
    total_savings,
    member_balance_sheet
)

urlpatterns = [
    path("", total_savings, name="savings"),
    path("<int:id>/", total_savings_details, name="savings-details"),
    path("members-savings/", members_savings, name="members-savings"),
    path("balance-sheet/", member_balance_sheet, name="balance-sheet"),
    path("pay-savings/", mark_member_savings_as_paid, name="member-savings-as-paid"),
    path("default-savings/<int:savings_id>/",mark_member_savings_as_defaulted, name="member-savings-as-defaulted"),
    path("reset-savings/<int:savings_id>/", mark_member_savings_as_reset, name="member-savings-as-reset"),
    path("cancel-savings/<int:savings_id>/", mark_member_savings_as_cancelled, name="member-savings-as-cancelled"),
]