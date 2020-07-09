from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
import string

# Create your models here.
class ShopUser(models.Model):
    user = models.OneToOneField(User,blank=False,null=False,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,unique=True)
    shop_type = models.CharField(max_length=20)
    active=models.BooleanField(default=False)
    premium=models.BooleanField(default=False)
    token=models.CharField(max_length=100,null=True,blank=True,unique=True)

    def __str__(self):
        return self.user.username

def generate(no=15):
    import random
    stri = string.digits + string.ascii_letters
    final = ''
    final = [random.choice(stri) for i in range(no)]
    return ''.join(final)

class Verification(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ver_token=models.CharField(max_length=50,unique=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    expired=models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        self.ver_token=generate(no=40)+str(self.user.id)
        super().save(*args,**kwargs)

def user_post_save_ver_creation(sender,instance,created,*args,**kwargs):
    if created:
        Verification.objects.create(user=instance)

post_save.connect(user_post_save_ver_creation,User)

def ver_post_save_mail(sender,instance,created,*args,**kwargs):
    if created:
        code="http://127.0.0.1:8000/register/activate/"+instance.ver_token
        send_mail("Verification",f"{code}\nThis link is valid for 10 minutes.",'<your email>',[instance.user.email])

post_save.connect(ver_post_save_mail,Verification)
