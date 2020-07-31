from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .forms import CustomerSignUpForm,AdminSignUpForm
from .models import User

from django.views.generic import TemplateView
from django.contrib import auth

def login(request):
    if request.method == 'POST':
        user=auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            if user.is_admin:
                return redirect('create')
            else:
                return redirect('/')
        else:
            return render(request, 'accounts/signup.html', {'error':'Username or password is incorrect'})


    else:
        return render(request, 'accounts/login.html')

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request,user)
        return redirect('/')

class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'accounts/signupp_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request,user)
        return redirect('create')



class SignUpView(TemplateView):
    template_name = 'accounts/signup.html'


def home1(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('create')
        else:
            return redirect('/')
    return render(request, 'accounts/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home1')
    else:
        return render(request, 'accounts/logout.html')
