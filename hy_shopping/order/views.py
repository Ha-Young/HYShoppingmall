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
from .serializers import OrderSerializer
from rest_framework import generics
from rest_framework import mixins

# Create your views here.


class OrderListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.all()

        # product queryset을 구한다
        product = self.request.query_params.get('product', None)
        product_querySet = Order.objects.all()

        if product != None:
            products = product.split(',')
            product_querySet = Order.objects.none()

            for product_one in products:
                product_querySet |= queryset.filter(product = product_one)

        # register_date queryset을 구한다
        register_date = self.request.query_params.get('register_date', None)
        register_date_querySet = Order.objects.all()

        if register_date != None:
            register_date_querySet = Order.objects.none()
            register_dates = register_date.split(',')

            for register_date_one in register_dates:
                register_date_querySet |= queryset.filter(register_date__contains = register_date_one)

        # hyuser queryset을 구한다
        hyuser = self.request.query_params.get('hyuser', None)
        hyuser_querySet = Order.objects.all()

        if hyuser != None:
            hyuser_querySet = Order.objects.none()
            hyusers = hyuser.split(',')
            print("here", hyusers)

            for hyuser_one in hyusers:
                hyuser_querySet |= queryset.filter(hyuser = hyuser_one)

        # quantity queryset을 구한다
        quantity = self.request.query_params.get('quantity', None)
        quantity_querySet = Order.objects.all()

        if quantity != None:
            print(quantity)
            quantity_querySet = Order.objects.filter(quantity=quantity)

        return product_querySet & register_date_querySet & hyuser_querySet & quantity_querySet

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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
