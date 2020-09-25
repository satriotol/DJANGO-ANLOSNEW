from django.contrib import admin
from .models import company,users,VacationModel,ImageDatasetModel,FaceRecognitionModel,PresenceModel

# Register your models here.
admin.site.register(company)
admin.site.register(ImageDatasetModel)
admin.site.register(FaceRecognitionModel)
admin.site.register(users)
admin.site.register(VacationModel)
admin.site.register(PresenceModel)