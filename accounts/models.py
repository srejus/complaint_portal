from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    USER_TYPE_CHOICES = (
        ('USER','USER'),
        ('HR','HR'),
        ('GOV_EMPLOYEE','GOV_EMPLOYEE'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    user_type = models.CharField(max_length=100,default='USER')
    address = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.full_name)