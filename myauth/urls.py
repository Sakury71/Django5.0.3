from django.urls import path

from . import views

app_name = "myauth"
urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('register/', views.register, name='register'),
    path('captcha',views.send_email_captcha,name='email_captcha')
]