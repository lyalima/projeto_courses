from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError
from datetime import date


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("full_name", "username", "cpf", "date_of_birth", "email", 
                  "telephone", "zip_code", "address", "neighborhood",
                  "city", "state", "education", "areas_of_interest")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.date_of_birth = self.cleaned_data["date_of_birth"]

        if commit:
            user.save()
        return user
    
    def clean_areas_of_interest(self):
        areas_of_interest = self.cleaned_data.get("areas_of_interest")

        if not self.instance.is_superuser and not areas_of_interest:
            raise ValidationError("Escolha pelo menos uma Área de Interesse.")
        return areas_of_interest
    
    def clean_date_of_birth(self):
        current_date = date.today()
        date_of_birth = self.cleaned_data.get("date_of_birth")

        if date_of_birth:
            if date_of_birth > current_date:
                raise ValidationError("Informe uma data válida")            
        else: 
            raise ValidationError("Informe uma data válida")
        return date_of_birth
    
    def clean_email(self):
        email_address = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email_address).exists():
            raise ValidationError(f'O email {email_address} já está vinculado a um usuário existente.')
        return email_address


class CustomUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário/Email', 
    )


class CustomReadOnlyPasswordHashWidget(forms.TextInput):

    def __init__(self, attrs=None):
        super().__init__(attrs={'readonly': 'readonly', **(attrs or {})})

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = "Senha ocultada para segurança."
        return super().render(name, value, attrs, renderer)


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(label="Senha", widget=CustomReadOnlyPasswordHashWidget)
        
    class Meta:
        model = CustomUser
        fields = ("photo", "username", "email", 
                  "telephone", "zip_code", "address", 
                  "neighborhood","city", 
                  "state", "education", "areas_of_interest")

    def clean_areas_of_interest(self):
        areas_of_interest = self.cleaned_data.get("areas_of_interest")
        if not self.instance.is_superuser and not areas_of_interest:
            raise ValidationError("Escolha pelo menos uma Área de Interesse.")
        
        return areas_of_interest
    
    def has_changed(self):
        return bool(self.changed_data)

    def save(self, commit=True):
        if self.has_changed():
            return super().save(commit)
        else:
            return self.instance


class CustomUserVerificationForm(forms.Form):
    code = forms.CharField(max_length=64)
