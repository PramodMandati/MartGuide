from django.urls import path
from .views import (
    register,DesktopCon,activation_user,home,contact,login_page,logout_page,login_home_page,download_soft,
    download_page,forget_password
    )
app_name='users_app_name'
urlpatterns = [
    path('home',home,name='home_url'),
    path('register',register,name='register_url'),
    path('register/activate/<slug:slug>',activation_user),
    path('contact',contact,name='contact_url'),


    path('login',login_page,name='login_url'),
    path('logout',logout_page,name='logout_url'),

    path('loginhome',login_home_page,name="login_home_url"),
    path('download',download_page,name='download_page_url'),
    path('download_app',download_soft,name='download_url'),
    path('reset',forget_password,name='password_url'),
    # path('recovery',forget_ps,name='recovery_url'),

    path('desktop',DesktopCon.as_view())
]