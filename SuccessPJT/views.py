from django.views.generic import TemplateView
from django.views.generic.edit import CreateView 
from .forms import CreateUserForm 
from django.urls import reverse_lazy
from django.shortcuts import render
import templates.registration

class CreateUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class= CreateUserForm

    
    success_url = reverse_lazy('create_user_done')

class RegisterdView(TemplateView):
    template_name ='registration/signup_done.html'


def pwreset(request):
    return render('password_reset_form.html')
