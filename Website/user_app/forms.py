from django import forms
from .models import ShopUser
from django.contrib.auth.models import User
class ShopUserForm(forms.ModelForm):
    class Meta:
        model=ShopUser
        fields=[
            'phone',
            'shop_type'
        ]

    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if len(phone)==10:
            try:
                phone=int(phone)
                sh=ShopUser.objects.filter(phone=phone)
                if int(sh.count())>0:
                    raise forms.ValidationError("Phone number already exists")
                return phone
            except TypeError:
                raise forms.ValidationError("Invalid phone number")
        else:
            raise forms.ValidationError("Invalid phone number")

class ShopUserForm2(forms.Form):
    username = forms.CharField(max_length=15,required=True)
    first_name=forms.CharField(max_length=15,required=True)
    last_name=forms.CharField(max_length=15,required=True)
    email=forms.EmailField(max_length=30,required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(),required=True)

    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=User.objects.filter(username=username)
        if qs.count()>0:
            raise forms.ValidationError("Username already exists")
        return username
    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=User.objects.filter(email=email)
        if qs.count():
            raise forms.ValidationError("Email already exists")
        return email
    def clean_confirm_password(self):
        pwd1=self.cleaned_data.get('password')
        pwd2=self.cleaned_data.get('confirm_password')
        if pwd1==pwd2:
            if not len(pwd2)>=8:
                raise forms.ValidationError("Not a strong password")
        else:
            raise forms.ValidationError("Passwords not matched")
        return pwd2

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class ResetForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.user=user
    old_password=forms.CharField(widget=forms.PasswordInput())
    new_password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    def clean_old_password(self):
        pwd=self.cleaned_data['old_password']
        if self.user.check_password(pwd):
            return pwd
        raise forms.ValidationError("incorrect password")

    def clean_confirm_password(self):
        pwd1=self.cleaned_data['new_password']
        pwd2=self.cleaned_data['confirm_password']
        if pwd1==pwd2:
            if len(pwd1)>=8:
                return pwd2
            raise forms.ValidationError('not a strong password')
        raise forms.ValidationError("password not matched")

