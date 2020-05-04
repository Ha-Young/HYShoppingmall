from django import forms

class RegisterForm(forms.Form):
    email = forms.EmailField(
        label="email",
        required=True, 
        error_messages={
            'required': '이메일을 입력하십시오'
        })
    password = forms.CharField(
        label="password",
        required=True, 
        error_messages={
            'required': '비밀번호를 입력하십시오'
        },
        widget=forms.PasswordInput)