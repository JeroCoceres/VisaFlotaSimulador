from django.contrib import admin
from costcenter.models import Cards,Transaction

@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ("is_costcenter","card_name","money")
    list_filter = ("is_costcenter",)
    search_fields = ("card_name",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("movement","movement_date","from_account","to_account")
    search_fields = ("from_account","to_account")