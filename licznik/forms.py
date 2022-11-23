
from django.contrib.auth import password_validation

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

from .models import *
from django.core.validators import FileExtensionValidator
from django.forms import DateInput
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.forms import TextInput,Select, ChoiceField


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nazwa użytkownika','style': 'width:300px'}),
        label="")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Hasło','style': 'width:300px'}),label='',)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'form-control', 'style': 'width:300px'}),label='')
    statue = forms.BooleanField(label='Zatwierdź regulamin')  # regulamin

class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, label='Login')
    first_name = forms.CharField(required=True, label='Pierwsze imię', help_text='Wymagany')
    second_name = forms.CharField(required=False, label='Drugie imię', help_text='Wymagany')
    last_name = forms.CharField(required=True, label='Nazwisko')
    pesel = forms.CharField(required=True, label='Pesel')
    email = forms.EmailField(required=True, label='Email')


    password1 = forms.CharField(
        label='Hasło',
        strip=False,
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Potwiedź hasło',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html())
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'form-control', 'style': 'width:300px'}),
                             label='')

    class Meta:
        model = User
        fields = ('username','password1','password2','first_name','second_name','last_name',"pesel",'email')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
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
class UserForm1(forms.ModelForm):
    email = forms.EmailField(max_length=254, widget=forms.Textarea(attrs={'rows':'1', 'cols':'50'}))
    username = forms.CharField(label='Nazwa użytkownika',widget=forms.Textarea(attrs={'rows':'1', 'cols':'50'}))
    first_name = forms.CharField(label='Imię', widget=forms.Textarea(attrs={'rows': '1', 'cols': '50'}))
    second_name = forms.CharField(label='Drugie imię', widget=forms.Textarea(attrs={'rows': '1', 'cols': '50'}))
    last_name = forms.CharField(label='Nazwisko', widget=forms.Textarea(attrs={'rows': '1', 'cols': '50'}))
    pesel = forms.CharField(label='Pesel', widget=forms.Textarea(attrs={'rows': '1', 'cols': '50'}))


    class Meta:
        model = User
        fields = ['username','first_name','second_name','last_name','email','pesel']
''' Formularz używany w admin '''

class UserForm2(forms.ModelForm):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput,help_text='Wymagany.')
    email = forms.EmailField(widget=forms.Textarea(attrs={'rows':'1', 'cols':'33'}) ,help_text='Wymagany.')
    class Meta:
        model = User
        fields = ['username','first_name','second_name','last_name','email','pesel','password']


    def save(self, commit=True):
        user = super(UserForm2, self).save(commit=False)
        print('user',user.password)
        user.password = make_password(user.password)
        if commit:
            user.save()
        return user

class UserForm(UserCreationForm):
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput,help_text='Wymagany.')
    password2 = forms.CharField(label='Potwierdż hasło', widget=forms.PasswordInput,help_text='Wymagany.')
    # password1 = None
    # password2 = None
    email = forms.EmailField(max_length=254, help_text='Wymagany.')
    class Meta:
        model = User
        fields = ['username','first_name','second_name','last_name','email','pesel']
class UserChangeForm(forms.ModelForm):
    # password = forms.CharField(label='Hasło', widget=forms.PasswordInput,help_text='Wymagany.')
    # password2 = forms.CharField(label='Potwierdż hasło', widget=forms.PasswordInput,help_text='Wymagany.')
    # password1 = None
    # password2 = None
    email = forms.EmailField(max_length=254, help_text='Wymagany.')
    class Meta:
        model = User
        fields = ['username','first_name','second_name','last_name','email','pesel']
        exclude =['is_staff']


class KandydatForm(forms.ModelForm):
    class Meta:
        model = Kandydat
        fields = ['clas','internat','j_pol_egz','mat_egz','j_obcy_egz','j_pol_oc','mat_oc','biol_oc',
                  'inf_oc','sw_wyr']

# class UserFormAdmin(forms.ModelForm):
#
#     firstname = forms.CharField()
#     secondname = forms.CharField()
#     lastname = forms.CharField()
#     pesel = forms.CharField()
#     # username = forms.CharField()
#     # password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta:
#         model = User
#         fields = '__all__'


# class KandydatFormAdmin(forms.ModelForm):
#     class Meta:
#         model = Kandydat
#         fields = '__all__'
#         # exclude = ["user"]

# ModelForm pobiera pole z modelu upload
class UploadForm(forms.Form):
    docfile = forms.FileField(
        label='Dołącz plik csv',
        help_text='max. 1MB',
        validators=[FileExtensionValidator(allowed_extensions=['csv'])])
class UploadForm1(forms.Form):
    docfile = forms.FileField(
        label='Dołącz plik csv',
        help_text='max. 1MB',
        validators=[FileExtensionValidator(allowed_extensions=['csv'])])



class StatusForm(forms.ModelForm):


    class Meta:

        # dt = statobj.datastart
        model = Status
        fields = ['status', 'datastart','dataend']
        widgets = {
            'datastart': DateInput(attrs={'type': 'date', 'value':datetime.datetime.today().strftime("%d-%m-%Y")}),
            'dataend': DateInput(attrs={'type': 'date'})
        }
