from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import ShopUserForm,ShopUserForm2,LoginForm,ResetForm
from .models import ShopUser,Verification
# Create your views here.
from django.utils import timezone
import bcrypt
import os

def home(request):
    if not request.user.is_authenticated:
        return render(request,'user_app/home.html',{'user':request.user})
    return redirect("user_app_name:login_home_url")

def register(request):
    if not request.user.is_authenticated:
        form=ShopUserForm(request.POST or None)
        form2=ShopUserForm2(request.POST or None)
        if form.is_valid() and form2.is_valid():
            user=User.objects.create_user(
                username=form2.cleaned_data.get('username'),
                email=form2.cleaned_data.get('email'),
                password=form2.cleaned_data.get('confirm_password'),
                first_name=form2.cleaned_data.get('first_name'),
                last_name=form2.cleaned_data.get('last_name'),
                is_active=False
                )
            s=ShopUser.objects.create(phone=form.cleaned_data.get('phone'),user=user,shop_type=form.cleaned_data.get('shop_type'))
            form = ShopUserForm()
            form2 = ShopUserForm2()
            return render(request,'user_app/success_reg.html',{'user':request.user})
        return render(request,'user_app/register.html',{'form':form,'form2':form2,'user':request.user})
    return redirect("user_app_name:login_home_url")


def activation_user(request,slug):
    try:
        ver = Verification.objects.get(ver_token=slug, expired=False)
        if ver.timestamp + timezone.timedelta(minutes=10) >= timezone.now():
            ver.expired = True
            ver.save()
            user = ver.user
            user.is_active = True
            user.save()
            mess='sucess'
        else:
            ver.expired = True
            ver.save()
            mess='expired'
    except:
        mess='invalid'
    return render(request,'user_app/sucess_invalid.html',{'msg':mess,'user':request.user})


def contact(request):
    if not request.user.is_authenticated:
        return render(request,"user_app/contact.html",{'user':request.user})
    return redirect("user_app_name:login_home_url")



def login_page(request):
    if request.user.is_authenticated:
        return redirect("user_app_name:login_home_url")
    else:
        form=LoginForm(request.POST or None)
        msg=''
        if form.is_valid():
            uname=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(username=uname,password=pwd)
            if user:
                login(request,user)
                return redirect('user_app_name:login_home_url')
            else:
                msg='invalid'
        return render(request,'user_app/loginpage.html',{'form':form,'msg':msg,'user':request.user})


@login_required(login_url='/login')
def login_home_page(request):
    return render(request, "user_app/homepagelogin.html", )

def download_page(request):
    if request.user.is_authenticated:
        if request.user.shopuser.premium:
            return render(request,'user_app/download_page2.html',{'user':request.user})
        return render(request,'user_app/download_page.html',{'user':request.user})
    return redirect("user_app_name:login_url")

def download_soft(request):
    if request.user.is_authenticated:
        response = HttpResponse(content_type='application/octet-stream')
        path = os.path.join(os.getcwd(), 'staticfiles/abc.exe')
        response['Content-Disposition'] = 'attachment;filename="abc.exe"'
        f = open(path, 'rb')
        response.write(f.read())
        f.close()
        return response
    return redirect("user_app_name:login_url")

def forget_password(request):
    if request.user.is_authenticated:
        form=ResetForm(request.user,data=request.POST or None)
        msg=''
        if form.is_valid():
            user=request.user
            user.set_password(request.POST.get('confirm_password'))
            user.save()
            user=authenticate(username=user.username,password=request.POST.get('confirm_password'))
            login(request,user)
            msg='success'
        return render(request,'user_app/resetpage.html',{'form':form,'msg':msg,'user':request.user})
    return redirect("user_app_name:login_url")


def logout_page(request):
    logout(request)
    return redirect("user_app_name:login_url")






from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class DesktopCon(APIView):
    def post(self, request):
        if request.data.get('status')=='logout':
            user=ShopUser.objects.filter(token=request.data.get('token'))
            user=user[0]
            user.token=None
            user.active=False
            user.save()
            return HttpResponse("logout")
        elif request.data.get('status')=='login_first':
            username = request.data.get('username')
            pwd=request.data.get('pwd')
            user = User.objects.filter(username=username,is_active=True).first()
            try:
                if user.check_password(pwd):
                    if not user.shopuser.active:
                        if user.shopuser.premium:
                            shop = user.shopuser
                            shop.active = True
                            token=bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
                            shop.token=token
                            shop.save()
                        else:
                            return HttpResponse(f"not a premium account")
                        return HttpResponse(f"login@{user.id}@{token}")
                    return HttpResponse("already loggedin")
                return HttpResponse("invalid username/password")
            except:
                return HttpResponse("invalid username/password")
        elif request.data.get('status') == 'login':
            user=ShopUser.objects.get(token=request.data.get('token'))
            if user:
                token = bcrypt.hashpw(user.user.password.encode(), bcrypt.gensalt())
                user.token=token
                user.active=True
                user.save()
                return HttpResponse(f'login@{user.user.id}@{token}')
            return HttpResponse('invalid')
