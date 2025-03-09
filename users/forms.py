from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']




from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class AdminUserEditForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Nueva Contraseña")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.password = make_password(password)  # Hashea la nueva contraseña
        if commit:
            user.save()
        return user