from django import forms
from costcenter.models import Cards,Transaction


class CardsForm(forms.ModelForm):
    class Meta:
        model = Cards
        fields = "__all__"


class DateInput(forms.DateInput):
    input_type = "date"

class TransactionForm(forms.ModelForm,DateInput):

    class Meta:
        model = Transaction
        fields = "__all__"
        widgets= {"movement_date":DateInput()}