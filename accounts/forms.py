
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from licznik.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox



class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Pierwsze imię', help_text='Wymagany')
    second_name = forms.CharField(required=False, label='Drugie imię', help_text='Wymagany')
    last_name = forms.CharField(required=True, label='Nazwisko')
    pesel = forms.CharField(required=True, label='Pesel')
    email = forms.EmailField(required=True, label='Email')
    username = forms.CharField(required=True, label='Login')

    password1 = forms.CharField(
        label='Hasło',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Potwiedź hasło',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ('first_name','second_name','last_name',"pesel",'username','email','password1','password2')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.pesel = self.cleaned_data["pesel"]
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.second_name = self.cleaned_data["second_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.password1 = self.cleaned_data["password1"]
        user.password2 = self.cleaned_data["password2"]

        if commit:
            user.save()
        return user



class UserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('username','pesel', 'email', 'first_name', 'second_name')