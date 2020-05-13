from django.shortcuts import render
from django.views.generic.edit import FormView
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

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.user_id

        return super().form_valid(form)