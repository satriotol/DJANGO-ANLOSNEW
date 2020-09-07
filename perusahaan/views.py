from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                CreateView,UpdateView,
                                DeleteView)
from perusahaan import models
from .models import users,presence
from perusahaan.forms import companyprofileform,CompanyForm,usersform
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework import viewsets,permissions,status,renderers,generics
from rest_framework.response import Response
from perusahaan.serializers import UserSerializer,UserProfileSerializer,UsersLocationSerializer,PresenceSerializer
# from shapely import geometry


# def check_polygon(request):
#     # users = models.users.objects.all().values('location')
#     users = models.users.objects.values_list('location', flat=True)

#     position = users
#     # position = [[-7.05294243391212,110.43200829993961],[-7.0531607107313,110.43192246925113],[-7.053394958910614,110.43223896991489],[-7.053134091612514,110.43231943618534]]

#     Point_X = -7.05304243391212
#     Point_Y = 110.43200829993961

#     line = geometry.LineString(position)
#     point = geometry.Point(Point_X, Point_Y)
#     polygon = geometry.Polygon(line)

#     # print(polygon.contains(point))

#     return HttpResponse(polygon.contains(point))
#     # return HttpResponse(position)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PresenceViewSet(viewsets.ModelViewSet):
    queryset = presence.objects.all()
    serializer_class = PresenceSerializer


@api_view(['GET','POST'])
def record_location_list(request):
    if request.method == 'GET':
        user_obj = users.objects.all()
        user_serializer = UsersLocationSerializer(user_obj, many=True)
        data =({
            "api_status" : 1,
            "api_message" : "success",
            "data" : user_serializer.data
        })
        return Response(data)

    elif request.method == 'POST':
        user_serializer = UsersLocationSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def record_location_detail(request,pk):
    try:
        user_obj = users.objects.get(pk=pk)
    except users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UsersLocationSerializer(user_obj)
        return Response(user_serializer.data)

    elif request.method == 'PUT':
        user_serializer = UsersLocationSerializer(user_obj, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RecordLocationViewSet(viewsets.ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UserProfileSerializer
    
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
        profile_form = companyprofileform(data=request.POST)

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
            return render(request,'login.html')
        else:
            
            print(user_form.errors,profile_form.errors)
    else:
        user_form = CompanyForm()
        profile_form = companyprofileform()

    return render(request,'perusahaan_form.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def registeruser(request):
    registered = False
    
    if request.method == "POST":
        user_form = CompanyForm(data=request.POST)
        profile_form = usersform(data=request.POST)

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
        profile_form = usersform()

    return render(request,'karyawan_form.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

@csrf_exempt
def user_login(request):
    context_object_name = 'data_login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
                # return JsonResponse(data,safe=False)
                # return HttpResponse(data)

            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and Password {}".format(username,password))
            # return HttpResponse("invalid login details supplied")
            messages.info(request, 'Username atau Password Yang Anda Inputkan Salah')
            return HttpResponseRedirect('/login/')
            # return render(request,'login.html')

    else:
        return render(request,'login.html',{'name' : request.user.username })

@csrf_exempt
def record_location(request):
    users = models.users.objects.all().values('id','id_company','location_office')
    data = json.dumps({
        "api_status": 1,
        "api_message": 'success',
        "data" : {
            "data" : list(users),
        }
    })
    
    return HttpResponse(data)

class EditUser(UpdateView):
    context_object_name = 'listusers'
    model = models.User
    fields = ['username','password']
    template_name = 'user_update.html'

class ProfilePerusahaan(ListView):
    context_object_name = 'profilperusahaan'
    model = models.company
    model = models.users
    template_name = 'profile.html'

class ListKaryawan(ListView):
    context_object_name = 'listkaryawans'
    model = models.users
    template_name = 'karyawan_list.html'

class DetailKaryawan(DetailView):
    model = models.users
    template_name = 'karyawan_detail.html'

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
