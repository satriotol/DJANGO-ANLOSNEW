from django import forms
from django.contrib.auth.models import User
from perusahaan.models import company,users,ImageDatasetModel

class ImageDatasetForm(forms.ModelForm):
    # ImageField = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta():
        model = ImageDatasetModel
        fields = ('user','file','file2','file3','file4','file5')

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

class companyprofileform(forms.ModelForm):
    class Meta():
        model = company
        fields = ('name','address','telp','location','start_work','end_work')

class usersform(forms.ModelForm):
    class Meta():
        model = users
        fields = ('id_company','is_company','name','telp','profile_pic','location','start_work','end_work')

class usercompanyprofileform(forms.ModelForm):
    class Meta():
        model = users
        fields = ('is_company','name','telp','location','start_work','end_work')