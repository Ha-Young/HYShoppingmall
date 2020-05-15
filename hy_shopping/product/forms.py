from django import forms
from .models import Product


class RegisterForm(forms.Form):
    name = forms.CharField(
        label="상품명",
        required=True, 
        error_messages={
            'required': '상품명을 입력하십시오'
        }
    )

    price = forms.CharField(
        label="상품가격",
        required=True, 
        error_messages={
            'required': '상품가격을 입력하십시오'
        }
    )

    description = forms.CharField(
        label="상품설명",
        required=True, 
        error_messages={
            'required': '상품설명을 입력하십시오'
        }
    )

    stock = forms.IntegerField(
        label="재고",
        required=True, 
        error_messages={
            'required': '재고를 입력하십시오'
        }  
    )

    def clean(self):
        print("clean")
        cleaned_data = super().clean()
        
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        description = cleaned_data.get('description')
        stock = cleaned_data.get('stock')

        if not (name and price and description and stock):
            self.add_error('name', '값이 없습니다.')
            self.add_error('price', '값이 없습니다.')
            self.add_error('description', '값이 없습니다.')
            self.add_error('stock', '값이 없습니다.')
