from django.urls import path
from savings.views import (
    members_savings,
    mark_member_savings_as_cancelled,
    mark_member_savings_as_paid,
    mark_member_savings_as_reset,
    mark_member_savings_as_defaulted,
    total_savings,
)

urlpatterns = [
    path("", total_savings, name="total-savings"),
    path("members-savings/", members_savings, name="members-savings"),
    path("member-savings-as-paid/", mark_member_savings_as_paid, name="member-savings-as-paid"),
    path("member-savings-as-defaulted/<int:savings_id>/",mark_member_savings_as_defaulted, name="member-savings-as-defaulted"),
    path("member-savings-as-reset/<int:savings_id>/", mark_member_savings_as_reset, name="member-savings-as-reset"),
    path("member-savings-as-canceled/<int:savings_id>/", mark_member_savings_as_cancelled, name="member-savings-as-cancelled"),
]