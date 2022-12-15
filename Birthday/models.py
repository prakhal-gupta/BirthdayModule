from django.db import models
from .models import *

class Student_Faculty_Profile(models.Model):
        Name                   = models.CharField(max_length=50, null=True)
        DOB                    = models.DateField(null=True)
        Email                  = models.EmailField(max_length= 80,null=True)
        Gender                 = models.CharField(max_length=20, null=True)
        Category               = models.CharField(max_length=20,default='Student')
        Current_Year           = models.CharField(max_length=20,null=True)
        Designation            = models.CharField(max_length=50,null=True)
        DOB_month              = models.CharField(max_length=5,null=True)
        DOB_day                = models.CharField(max_length=5,null=True)
        Profile_pic            = models.ImageField(upload_to='Profile_pic/', default='static/profile-default.png')


class Birthday_Message(models.Model):
        Content                = models.TextField()

class Otp_Verification(models.Model):
        Email                  = models.EmailField(max_length=80)
        OTP                    = models.CharField(max_length=20,null=True)
        
