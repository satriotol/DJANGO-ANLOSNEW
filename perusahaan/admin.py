from django.contrib import admin
from .models import company,company_privileges,users,vacation

# Register your models here.
admin.site.register(company)
admin.site.register(company_privileges)
admin.site.register(users)
admin.site.register(vacation)



