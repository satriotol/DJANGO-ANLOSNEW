from django.contrib import admin
from .models import company,company_privileges,users,vacation,presence,ImageDatasetModel,FaceRecognitionModel

# Register your models here.
admin.site.register(company)
admin.site.register(ImageDatasetModel)
admin.site.register(FaceRecognitionModel)
admin.site.register(users)
admin.site.register(vacation)
admin.site.register(presence)




