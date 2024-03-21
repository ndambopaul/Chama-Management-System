from django.urls import path
from finance.views import (
    payments,
    new_payment,
    chama_rounds,
    new_chama_round,
    members_savings,
    chama_round_payments,
    mark_chama_payments_as_paid,
    mark_chama_payments_as_defaulted,
    mark_chama_payments_as_cancelled,
    mark_chama_payments_as_reset,
    mark_member_savings_as_cancelled,
    mark_member_savings_as_paid,
    mark_member_savings_as_reset,
    mark_member_savings_as_defaulted,

    end_chama_round,
    delete_chama_round,
    chama_fines
)

urlpatterns = [
    path("payments/", payments, name="payments"),
    path("new-payment/", new_payment, name="new-payment"),
    path("chama-rounds/", chama_rounds, name="chama-rounds"),
    path("new-chama-round/", new_chama_round, name="new-chama-round"),
    path("end-round/<int:chama_round_id>", end_chama_round, name="end-chama-round"),
    path("delete-round/", delete_chama_round, name="delete-chama-round"),

    path("members-savings/", members_savings, name="members-savings"),
    path("member-savings-as-paid/", mark_member_savings_as_paid, name="member-savings-as-paid"),
    path("member-savings-as-defaulted/<int:savings_id>/", mark_member_savings_as_defaulted, name="member-savings-as-defaulted"),
    path("member-savings-as-reset/<int:savings_id>/", mark_member_savings_as_reset, name="member-savings-as-reset"),
    path("member-savings-as-canceled/<int:savings_id>/", mark_member_savings_as_cancelled, name="member-savings-as-cancelled"),

    path("chama-payments/", chama_round_payments, name="chama-payments"),
    path(
        "chama-payment-as-paid/<int:payment_id>/",
        mark_chama_payments_as_paid,
        name="chama-payment-as-paid",
    ),
    path(
        "chama-payment-as-defaulted/<int:payment_id>/",
        mark_chama_payments_as_defaulted,
        name="chama-payment-as-defaulted",
    ),
    path(
        "chama-payment-as-reset/<int:payment_id>/",
        mark_chama_payments_as_reset,
        name="chama-payment-as-reset",
    ),
    path(
        "chama-payment-as-cancelled/<int:payment_id>/",
        mark_chama_payments_as_cancelled,
        name="chama-payment-as-cancelled",
    ),
    path("chama-fines/", chama_fines, name="chama-fines"),
]
