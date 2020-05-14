from django import forms
from .models import Order
from product.models import Product
from hyuser.models import Hyuser


class RegisterForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(
        label="수량",
        required=True, 
        error_messages={
            'required': '수량을 입력하십시오'
        }
    )

    product = forms.IntegerField(
        label="상품설명",
        required=True, 
        error_messages={
            'required': '상품설명을 입력하십시오'
        },
        widget=forms.HiddenInput
    )

    def clean(self):
        print("clean")
        cleaned_data = super().clean()
        
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        hyuser = self.request.session.get('user')

        if quantity and product and hyuser:
            order = Order(
                quantity=quantity,
                product=Product.objects.get(pk=product),
                hyuser=Hyuser.objects.get(pk=hyuser)
            )

            order.save()
        else:
            self.product = product
            self.add_error('quantity', '값이 없습니다')
            self.add_error('product', '값이 없습니다')
