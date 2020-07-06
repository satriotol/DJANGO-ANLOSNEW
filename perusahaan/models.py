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
    location = models.TextField(max_length=256)

    def __str__(self):
        return self.name

class users(models.Model):
    # id_company = models.ForeignKey(company,on_delete=models.CASCADE,default='')
    # id_company = models.ManyToManyField(company)
    user = models.OneToOneField(User,related_name="users",on_delete=models.CASCADE,default="")
    id_company = models.IntegerField()
    name = models.CharField(max_length=254)
    # email = models.EmailField()
    telp = models.CharField(max_length=12)


    def __str__(self):
        return self.name

class presence(models.Model):
    id_user = models.IntegerField()
    date_presence = models.DateField()
    start_presence = models.TimeField()
    end_presence = models.TimeField()
    location = models.TextField(max_length=256)

class vacation (models.Model):
    id_user = models.ForeignKey(users,on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()