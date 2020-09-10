from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class company_privileges(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name
class company(models.Model):
    user = models.OneToOneField(User,related_name="company",on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    telp = models.CharField(max_length=12)
    location = models.TextField(default="")
    start_work = models.TimeField(null=True)
    end_work = models.TimeField(null=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="users",on_delete=models.CASCADE,default="")
    id_company = models.IntegerField()
    is_company = models.IntegerField()
    name = models.CharField(max_length=254)
    telp = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    location = models.TextField(default="")
    record_location = models.TextField(null=True)
    start_work = models.TimeField(null=True)
    end_work = models.TimeField(null=True)

    def __str__(self):
        return self.name

class presence(models.Model):
    id_user = models.IntegerField()
    id_company = models.IntegerField()
    date_presence = models.DateField()
    start_presence = models.TimeField(null=True)
    end_presence = models.TimeField(null=True)

class vacation (models.Model):
    id_user = models.ForeignKey(users,on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()