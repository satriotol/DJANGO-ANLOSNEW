from django import forms
from django.contrib.auth.models import User
from perusahaan.models import company,users

class CompanyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password','groups')

class company(forms.ModelForm):
    class Meta():
        model = company
        fields = ('name','address','telp','location')

class users(forms.ModelForm):
    class Meta():
        model = users
        fields = ('id_company','name','telp')