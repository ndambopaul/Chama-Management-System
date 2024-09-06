from django.contrib import admin
from savings.models import GroupedSaving
from finance.models import MemberSaving
# Register your models here.
@admin.register(GroupedSaving)
class GroupSavingAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "member", "start_date", "end_date", "amount_saved", "redeemed", "active"]

@admin.register(MemberSaving)
class MemberSavingAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "member", "saving", "amount_saved", "amount_fined"]