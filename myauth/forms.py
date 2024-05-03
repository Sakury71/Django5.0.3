from django import forms
from django.contrib.auth import get_user_model

from .models import Captcha

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3, error_messages={
        'required': '用户名不能为空',
        'max_length': '用户名不能超过20个字符',
        'min_length': '用户名不能少于3个字符'
    })
    email = forms.EmailField(error_messages={"required": "请传入邮箱！", 'invalid': '请传入一个正确的邮箱！'})
    captcha = forms.CharField(max_length=4, min_length=4, error_messages={
        'required': '验证码不能为空',
        'max_length': '验证码不能超过4个字符',
        'min_length': '验证码不能少于4个字符'
    })
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过20个字符',
        'min_length': '密码不能少于6个字符'
    })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已被注册！')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        captcha_model = Captcha.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('邮箱与验证码不匹配！')
        captcha_model.delete()
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": "请传入邮箱！", 'invalid': '请传入一个正确的邮箱！'})
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'required': '密码不能为空',
        'max_length': '密码不能超过20个字符',
        'min_length': '密码不能少于6个字符'
    })
    remember = forms.IntegerField(required=False)
