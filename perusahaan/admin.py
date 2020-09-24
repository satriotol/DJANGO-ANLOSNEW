from django.contrib import admin
from .models import company,users,vacation,ImageDatasetModel,FaceRecognitionModel,PresenceModel

# Register your models here.
admin.site.register(company)
admin.site.register(ImageDatasetModel)
admin.site.register(FaceRecognitionModel)
admin.site.register(users)
admin.site.register(vacation)
admin.site.register(PresenceModel)