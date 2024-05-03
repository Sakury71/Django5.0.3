import random
import string

from django.contrib.auth import get_user_model, login, logout
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, LoginForm
from .models import Captcha

User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def mylogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录成功
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print('邮箱或密码错误！')
                # form.add_error('email', '邮箱或密码错误！')
                # return render(request, 'login.html', context={'form': form})
                return redirect(reverse('myauth:login'))


def mylogout(request):
    # 退出登录功能
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('myauth:login'))
        else:
            print(form.errors)
            # 跳转到注册页面
            return redirect(reverse('myauth:register'))
            # return render(request, 'register.html', context={'form': form})


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": "必须传递邮箱！"})
    # 生成验证码（取随机的4位阿拉伯数字）
    captcha = "".join(random.sample(string.digits, 4))
    # 将邮箱验证码保存到MYSQL数据库当中去
    Captcha.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail('MYBLOG注册验证码', message=f'您的注册验证码是：{captcha}', from_email=None, recipient_list=[email])
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})
