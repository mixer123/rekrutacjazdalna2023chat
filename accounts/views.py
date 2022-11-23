from django.shortcuts import render

# Create your views here.

# from django.contrib.auth.forms import UserCreationForm
from accounts.forms import UserForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form = UserForm
    success_url = reverse_lazy('success')
    template_name = 'registration/signup.html'

def success(request):
    return render(request, 'registration/success.html')