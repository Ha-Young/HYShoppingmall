from django import forms
from .models import Order


class RegisterForm(forms.Form):
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
        