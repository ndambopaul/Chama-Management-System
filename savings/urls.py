from django.urls import path
from savings.views import (
    members_savings,
    total_savings_details,
    mark_member_savings_as_cancelled,
    mark_member_savings_as_paid,
    mark_member_savings_as_reset,
    mark_member_savings_as_defaulted,
    total_savings,
    member_balance_sheet,
    payout_member_savings,
    create_savings_period,
    savings_payouts
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

    path("payout-member-savings/", payout_member_savings, name="payout-member-savings"),
    path("create-savings-period/", create_savings_period, name="create-savings-period"),
    path("savings-payouts/", savings_payouts, name="savings-payouts"),
]