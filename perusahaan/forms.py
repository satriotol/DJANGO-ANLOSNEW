from django import forms
from django.contrib.auth.models import User
from perusahaan.models import company,users,ImageDatasetModel,VacationModel


class VacationForm(forms.ModelForm):
    class Meta():
        model = VacationModel
        fields= ('vacation_status',)

class ImageDatasetForm(forms.ModelForm):
    # ImageField = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta():
        model = ImageDatasetModel
        fields = ('user','file','file2','file3','file4','file5','file6','file7','file8','file9','file10')

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
        fields = ('id_company','is_company','name','telp','profile_pic')

class usercompanyprofileform(forms.ModelForm):
    class Meta():
        model = users
        fields = ('is_company','name','telp')

class ContactForm(forms.Form):
    to_email = forms.EmailField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)