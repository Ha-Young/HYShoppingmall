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
import datetime

# Create your views here.

def getProductQuerySet(req):
    product = req.query_params.get('product', None)
    print(product)
    product_querySet = Order.objects.all()

    if product != None:
        products = product.split(',')
        product_querySet = Order.objects.none()

        for product_one in products:
            product_querySet |= Order.objects.filter(product = product_one)
    
    return product_querySet

def getRegisterDateQuerySet(req):
    register_date = req.query_params.get('register_date', None)
    register_date_querySet = Order.objects.all()

    if register_date != None:
        register_date_querySet = Order.objects.none()
        register_dates = register_date.split(',')

        for register_date_one in register_dates:
            register_date_querySet |= Order.objects.filter(register_date__contains = register_date_one)
    
    return register_date_querySet

def getHyuserQuerySet(req):
    hyuser = req.query_params.get('hyuser', None)
    hyuser_querySet = Order.objects.all()

    if hyuser != None:
        hyuser_querySet = Order.objects.none()
        hyusers = hyuser.split(',')
        print("here", hyusers)

        for hyuser_one in hyusers:
            hyuser_querySet |= Order.objects.filter(hyuser = hyuser_one)

    return hyuser_querySet

def getQuantityQuerySet(req):
    quantity = req.query_params.get('quantity', None)
    quantity_querySet = Order.objects.all()

    if quantity != None:
        print(quantity)
        quantity_querySet = Order.objects.filter(quantity=quantity)
    
    return quantity_querySet


class OrderListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.all()

        # product queryset을 구한다
        product_querySet = getProductQuerySet(self.request)
        

        # register_date queryset을 구한다
        register_date_querySet = getRegisterDateQuerySet(self.request)

        # hyuser queryset을 구한다
        hyuser_querySet = getHyuserQuerySet(self.request)

        # quantity queryset을 구한다
        quantity_querySet = getQuantityQuerySet(self.request)

        return product_querySet & register_date_querySet & hyuser_querySet & quantity_querySet

        # 주문의 기간 (시작 . 끝 ) / 시작이 없으면 처음, 끝이 없으면 오늘날
        # ToDo
        startday = self.request.query_params.get('startday', None)
        endday = self.request.query_params.get('endday', None)
        
        if startday != None:
            startday_split = startday.split('-')
            if len(startday_split) == 3:
                startday = datetime.date(startday_split[0], startday_split[1], startday_split[2])
            else:
                startday = datetime.date.today()
        else:
            startday = datetime.date.today()

        # 주문 가격 (시작 ~ 끝) / 시작이 없으면 끝값 이하, 끝이 없으면 시작 이상

        # 제품명

        # 제품가격

        # 제품 총개수 -> 다른곳?

        # email 주소 특정 도매인

        # 특정 기간에 가입한

        # ordering

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
