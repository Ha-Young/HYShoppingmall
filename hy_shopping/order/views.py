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
from . import query

# Create your views here.

class OrderListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = OrderSerializer
    
    def get_queryset(self):

        # product queryset을 구한다
        product_querySet = query.getProductQuerySet(self.request)
        
        # register_date queryset을 구한다
        register_date_querySet = query.getRegisterDateQuerySet(self.request)

        # hyuser queryset을 구한다
        hyuser_querySet = query.getHyuserQuerySet(self.request)

        # quantity queryset을 구한다
        quantity_querySet = query.getQuantityQuerySet(self.request)

        # date range queryset을 구한다
        # 주문의 기간 (시작 . 끝 ) / 시작이 없으면 처음, 끝이 없으면 오늘날
        dateRangeQuerySet = query.getDateRangeQuerySet(self.request)

        # order price range queryset을 구한다
        # 주문 가격 (시작 ~ 끝) / 시작이 없으면 끝값 이하, 끝이 없으면 시작 이상
        orderPriceRangeQuerySet = query.getOrderPriceRangeQuerySet(self.request)

        querySet = product_querySet\
                & register_date_querySet\
                & hyuser_querySet\
                & quantity_querySet\
                & dateRangeQuerySet\
                & orderPriceRangeQuerySet
        
        # ordering
        querySet = query.getOrderingQuerySet(self.request, querySet)
        
        return querySet
        

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
                productObj = Product.objects.get(pk=form.data.get('product'))
                quantity = int(form.data.get('quantity'))
                price = productObj.price * quantity
                order = Order(
                    quantity = quantity,
                    product = productObj,
                    hyuser = Hyuser.objects.get(pk=self.request.session.get('user')),
                    price = price
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
