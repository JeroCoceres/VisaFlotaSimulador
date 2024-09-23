from django import forms
from costcenter.models import Cards,Transaction
from datetime import datetime, timedelta


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


class MesesForm(forms.Form):
    periodo = forms.ChoiceField(label="Periodo")

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            hoy = datetime.today()
            opciones_meses = [(hoy - timedelta(days=30*i)).strftime("%m-%Y") for i in range(12)]
            self.fields['periodo'].choices = [(mes, mes) for mes in opciones_meses]