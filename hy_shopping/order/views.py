from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db import transaction
from .models import Order
from .forms import RegisterForm
from product.models import Product
from hyuser.models import Hyuser
from hyuser.decorator import login_required

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
                productObj = Product.objects.get(pk=form.data.get('product'))
                order = Order(
                    quantity=form.data.get('quantity'),
                    product=productObj,
                    hyuser=Hyuser.objects.get(pk=self.request.session.get('user'))
                )
                order.save()
                productObj.stock -= int(form.data.get('quantity'))
                productObj.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request':self.request
        })
        return kw


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(hyuser__id=self.request.session.get('user'))
        return queryset
