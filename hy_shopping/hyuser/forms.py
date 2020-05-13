from django import forms
from .models import Hyuser
from django.contrib.auth.hashers import check_password, make_password


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label="이메일",
        required=True, 
        error_messages={
            'required': '이메일을 입력하십시오'
        }
    )

    password = forms.CharField(
        label="비밀번호",
        required=True, 
        error_messages={
            'required': '비밀번호를 입력하십시오'
        },
        widget=forms.PasswordInput
    )

    re_password = forms.CharField(
        label="비밀번호 확인",
        required=True, 
        error_messages={
            'required': '비밀번호를 입력하십시오'
        },
        widget=forms.PasswordInput
    )

    def clean(self):
        print("clean")
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        print(password, re_password)

        if password and re_password:
            if password != re_password:
                print("not same")
                self.add_error('password', '비밀번호가 서로 다릅니다')
                self.add_error('re_password', '비밀번호가 서로 다릅니다')
                return
            else:
                new_hyuser = Hyuser(
                                email=email,
                                password=make_password(password)
                )

                new_hyuser.save()


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="이메일",
        required=True, 
        error_messages={
            'required': '이메일을 입력하십시오'
        }
    )

    password = forms.CharField(
        label="비밀번호",
        required=True, 
        error_messages={
            'required': '비밀번호를 입력하십시오'
        },
        widget=forms.PasswordInput
    )

    def clean(self):
        print("clean")
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        print(email, password)

        if email and password:
            try:
                hyuser = Hyuser.objects.get(email=email)
            # except Hyuser.DoseNotExist as e:
            #     print(e)
            #     self.add_error('email', '없는 email 입니다')
            #     return
            except Exception as e:
                print(e)
                self.add_error('email', '알수없는 오류')
                return

            if not check_password(password, hyuser.password):
                self.add_error('password', '비밀번호를 틀렸습니다')
            else:
                self.user_id = hyuser.id