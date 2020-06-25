from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                CreateView,UpdateView,
                                DeleteView)
from perusahaan import models
from perusahaan.forms import company,CompanyForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

class IndexPerusahaan(ListView):
    model = models.company
    template_name = 'index.html'

def registercompany(request):
    registered = False
    
    if request.method == "POST":
        user_form = CompanyForm(data=request.POST)
        profile_form = company(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = CompanyForm()
        profile_form = company()

    return render(request,'perusahaan_form.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    context_object_name = 'data_login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and Password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'login/login.html',{'name' : request.user.username })
# class BuatDataPerusahaan(CreateView):
#     model = models.company
#     fields = ('name','address','email','telp','location')
#     template_name = 'perusahaan_form.html'
#     success_url = reverse_lazy('index')
