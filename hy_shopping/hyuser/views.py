from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegisterForm
from .forms import LoginForm
from .models import Hyuser

# Create your views here.


def index(request):
    user_id = request.session.get('user')
    if user_id:
        hyuser = Hyuser.objects.get(id=request.session.get('user'))
        if hyuser:
            return render(request, 'index.html', {'email': hyuser.email})

    return render(request, 'index.html')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        new_hyuser = Hyuser(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
            level="user"
        )
        new_hyuser.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.user_id

        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del request.session['user']

    return redirect('/')