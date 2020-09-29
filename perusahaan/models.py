from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
class company(models.Model):
    user = models.OneToOneField(User,related_name="company",on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    telp = models.CharField(max_length=12)
    location = models.TextField(default="")
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    start_work = models.TimeField(null=True)
    end_work = models.TimeField(null=True)

    def __str__(self):
        return self.user.username

class users(models.Model):
    user = models.OneToOneField(User,related_name="users",on_delete=models.CASCADE,default="")
    id_company = models.ForeignKey(company, on_delete=models.CASCADE)
    is_company = models.IntegerField(default="0")
    name = models.CharField(max_length=254)
    telp = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    # location = models.TextField(default="")
    # start_work = models.TimeField(null=True)
    # end_work = models.TimeField(null=True)

    def __str__(self):
        return self.name
class PresenceModel(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_company = models.ForeignKey(company, on_delete=models.CASCADE)
    date_presence = models.DateField()
    start_presence = models.TimeField(null=True)
    end_presence = models.TimeField(null=True)
    durasi_kerja = models.DurationField(null=True)
    def __str__(self):
        return self.id_user.username


class VacationModel (models.Model):
    SAKIT = 'SAKIT'
    IJIN = 'IJIN'
    LAIN = 'LAIN'
    VACATION_CHOICE = [
        (SAKIT, 'SAKIT'),
        (IJIN, 'IJIN'),
        (LAIN, 'LAIN'),
    ]
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    STATUS_CHOICE =[
        (PENDING,'PENDING'),
        (ACCEPTED,'ACCEPTED'),
        (REJECTED,'REJECTED'),
    ]

    id_user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_company = models.ForeignKey(company,on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()
    vacation_type = models.CharField(choices=VACATION_CHOICE,max_length=5)
    message = models.TextField(max_length=500)
    vacation_status = models.CharField(choices=STATUS_CHOICE,max_length=8,default="PENDING")

def get_upload_path(instance, filename):
    return os.path.join(
        "image_field/%s" % instance.user.id,filename)

class ImageDatasetModel (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,default="")
    file = models.FileField(upload_to=get_upload_path,default="")
    file2 = models.FileField(upload_to=get_upload_path,default="")
    file3 = models.FileField(upload_to=get_upload_path,default="")
    file4 = models.FileField(upload_to=get_upload_path,null=True,blank=True)
    file5 = models.FileField(upload_to=get_upload_path,null=True,blank=True)
    file6 = models.FileField(upload_to=get_upload_path,null=True,blank=True)
    file7 = models.FileField(upload_to=get_upload_path,null=True,blank=True)
    file8 = models.FileField(upload_to=get_upload_path,null=True,blank=True)
    file9 = models.FileField(upload_to=get_upload_path,null=True,blank=True)
    file10 = models.FileField(upload_to=get_upload_path,null=True,blank=True)

    def __str__(self):
        return self.user.username

class FaceRecognitionModel (models.Model):
    image = models.ImageField(upload_to='FaceRecognition_Dataset')
    created_at = models.DateTimeField(auto_now_add=True)