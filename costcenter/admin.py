from django.contrib import admin
from costcenter.models import Cards,Transaction

@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ("is_costcenter","card_name","money",'card_number')
    list_filter = ("is_costcenter",)
    search_fields = ("card_name",)
    exclude = ('card_number',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si está editando un objeto existente
            return self.readonly_fields + ('is_costcenter',)
        return self.readonly_fields


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("movement_date","from_account","to_account")
    search_fields = ("from_account","to_account")