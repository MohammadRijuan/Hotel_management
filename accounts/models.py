from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True)
    birth_date = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10,choices=[
        ('Male','Male'),
        ('Female','Female'),
    ])
    balance = models.DecimalField(default=0,max_digits=12, decimal_places=2)
    initial_deposit_date =models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.account_no)
    

class UserAddress(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=110)
    country = models.CharField(max_length=80)

    def __str__(self):
        return self.user.username
