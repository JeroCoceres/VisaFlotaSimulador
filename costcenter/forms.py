from django import forms
from costcenter.models import Cards,Transaction


class CardsForm(forms.ModelForm):
    class Meta:
        model = Cards
        fields = "__all__"


class DateInput(forms.DateInput):
    input_type = "date"


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['from_account', 'to_account', 'amount']




class FundTransferForm(forms.Form):
    card_number = forms.IntegerField(widget=forms.HiddenInput())
    amount = forms.FloatField(label='Monto a transferir', min_value=0)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return amount

