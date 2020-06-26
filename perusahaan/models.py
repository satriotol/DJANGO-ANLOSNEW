from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class company_privileges(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name
class company(models.Model):
    user = models.ForeignKey(User,default='',related_name="company",on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    telp = models.CharField(max_length=12)
    location = models.TextField(max_length=256)

    def __str__(self):
        return self.name

class users(models.Model):
    id_company = models.ForeignKey(company,on_delete=models.CASCADE)
    id_privilege = models.ForeignKey(company_privileges,on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    email = models.EmailField()
    telp = models.CharField(max_length=12)

    def __str__(self):
        return self.name 

class vacation (models.Model):
    id_user = models.ForeignKey(users,on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()