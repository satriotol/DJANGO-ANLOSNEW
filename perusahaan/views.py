from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                CreateView,UpdateView,
                                DeleteView)
from perusahaan import models
from perusahaan.forms import company,CompanyForm,users
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.decorators.csrf import csrf_exempt





# Create your views here.
def special (request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
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

def registeruser(request):
    registered = False
    
    if request.method == "POST":
        user_form = CompanyForm(data=request.POST)
        profile_form = users(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = CompanyForm()
        profile_form = users()

    return render(request,'karyawan_form.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

@csrf_exempt
def user_login(request):
    user = models.User.objects.all().values('username','password')
    # data = serializers.serialize('json', user)
    data = json.dumps({
        "api_status": 1,
        "api_message": 'success',
        "data": list(user)
    })
    

    context_object_name = 'data_login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                # return HttpResponseRedirect(reverse('index'))
                # return JsonResponse(data,safe=False)
                return HttpResponse(data)

            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and Password {}".format(username,password))
            # return HttpResponse("invalid login details supplied")
            return render(request,'login.html')
    else:
        return render(request,'login.html',{'name' : request.user.username })

@csrf_exempt
def user_login_api(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = models.User.objects.filter(username=username).values('username','password')
    # data = serializers.serialize('json', user)
    data = json.dumps({
        "api_status": 1,
        "api_message": 'success',
        "data": list(user)
    })
    

    context_object_name = 'data_login'
    if request.method == 'GET':
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                # return HttpResponseRedirect(reverse('index'))
                # return JsonResponse(data,safe=False)
                return HttpResponse(data)

            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and Password {}".format(username,password))
            # return HttpResponse("invalid login details supplied")
            return HttpResponse(data)
    else:
        return HttpResponse(data)

class ProfilePerusahaan(ListView):
    context_object_name = 'profilperusahaan'
    model = models.company
    model = models.users
    template_name = 'profile.html'

class ListKaryawan(ListView):
    context_object_name = 'listkaryawans'
    model = models.users
    template_name = 'karyawan_list.html'

class ListKaryawanDeleteView(DeleteView):
    context_object_name = 'listkaryawans'
    model = models.users
    template_name = 'karyawan_confirm_delete.html'
    success_url = reverse_lazy('listkaryawan')

class ListKaryawanUpdateView(UpdateView):
    fields = ('name','telp')
    model = models.users
    template_name = 'karyawan_update.html'
    success_url = reverse_lazy('listkaryawan')

class ListVacation(ListView):
    context_object_name = 'listvacations'
    model = models.vacation
    template_name = 'vacation_list.html'
