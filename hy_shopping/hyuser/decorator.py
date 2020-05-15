from django.shortcuts import redirect
from .models import Hyuser

def login_required(func):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login/')
        return func(request, *args, **kwargs)

    return wrap

def admin_required(func):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login/')

        user = Hyuser.objects.get(pk=user)
        print(user.level)
        if user.level != 'admin':
            print("redircet")
            return redirect('/')
        
        return func(request, *args, **kwargs)

    return wrap
