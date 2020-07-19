from django import forms
from django.contrib.auth.models import User
from perusahaan.models import company,users

class CompanyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password','groups')

    def clean(self):
        cleaned_data = super(CompanyForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class company(forms.ModelForm):
    class Meta():
        model = company
        fields = ('name','address','telp','location')

class users(forms.ModelForm):
    class Meta():
        model = users
        fields = ('id_company','name','telp')