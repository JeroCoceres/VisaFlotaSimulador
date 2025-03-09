from django import forms
from costcenter.models import Cards,Transaction, Consumo
from datetime import datetime, timedelta
from django.utils import timezone


from django import forms
from costcenter.models import Cards

class CardsForm2(forms.ModelForm):
    class Meta:
        model = Cards
        fields = ['card_name', 'is_costcenter', 'money']





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

class ConsumoForm(forms.ModelForm):
    class Meta:
        model = Consumo
        fields = ['tipo_de_gasto', 'cantidad', 'un_med', 'clase', 'monto_parcial', 'nro_factura', 'nro_movil', 'odometro']

class MesesForm(forms.Form):
    periodo = forms.ChoiceField(label='Periodo', choices=[])

    def __init__(self, *args, **kwargs):
        super(MesesForm, self).__init__(*args, **kwargs)
        
        # Utilizar timezone.now() de Django
        ahora = timezone.now()
        ultimo_mes = ahora - timedelta(days=ahora.day)  # Último día del mes anterior
        choices = []
        
        # Iterar desde el mes pasado hasta un año antes
        for i in range(12):
            mes = ultimo_mes.month
            anio = ultimo_mes.year
            choices.append((f"{mes:02d}-{anio}", f"{mes:02d}-{anio}"))
            ultimo_mes -= timedelta(days=ultimo_mes.day)  # Retrocede un mes

        self.fields['periodo'].choices = choices



