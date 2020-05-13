from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import Product
from .forms import RegisterForm

# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'

class ProductCreate(FormView):
    model = Product
    template_name = 'register_product.html'
    context_object_name = 'product_list'
    form_class = RegisterForm
    success_url = '/product/'

class ProductDetail(DetailView):
    model = Product
    template_name = 'detail_product.html'
    queryset = Product.objects.all()
    context_object_name = 'product'