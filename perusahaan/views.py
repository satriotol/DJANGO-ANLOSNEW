from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                CreateView,UpdateView,
                                DeleteView)
from perusahaan import models
from .models import users,presence,company,ImageDatasetModel
from django.views.generic.edit import FormView
from perusahaan.forms import companyprofileform,CompanyForm,usersform,usercompanyprofileform,ImageDatasetForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum
from django.utils.decorators import method_decorator
from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework import viewsets,permissions,status,renderers,generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from perusahaan.serializers import UserSerializer,UserProfileSerializer,UsersLocationSerializer,PresenceSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count



class ImageFieldView(CreateView):
    form_class = ImageDatasetForm
    model = models.users
    context_object_name = 'listkaryawans'
    template_name = 'upload.html'
    success_url = reverse_lazy('upload')

    def get_context_data(self, **kwargs):
        context = super(ImageFieldView, self).get_context_data(**kwargs)
        context['userslist'] = users.objects.all()
        return context

# class ImageFieldView(View):
#     def get(self, request):
#         photo_list = ImageDatasetModel.objects.all()
#         return render(self.request, 'upload.html',{'photos':photo_list})

#     def post(self,request):
#         form = ImageDatasetForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             photo  = form.save()
#             data = {'is_valid': True, 'name':photo.file.name, 'url':photo.file.url}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username','email']

class UserDetail(generics.RetrieveAPIView):
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
    return HttpResponseRedirect(reverse('user_login'))

class IndexPerusahaan(ListView):
    model = models.users
    context_object_name = 'listkaryawans'
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexPerusahaan, self).get_context_data(**kwargs)
        context['userslist'] = users.objects.annotate(total=Count('id_company')).filter(is_company=1)
        context['companylist'] = users.objects.annotate(total=Count('id_company')).filter(is_company=0)
        return context


def registercompany(request):
    registered = False
    
    if request.method == "POST":
        user_form = CompanyForm(data=request.POST)
        profile_form = usercompanyprofileform(data=request.POST)

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
        profile_form = usercompanyprofileform()

    return render(request,'perusahaan_form.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def registeruser(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    else:
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
            messages.info(request, 'Username atau Password Yang Anda Inputkan Salah')
            return HttpResponseRedirect('/login/')
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

class ProfilePerusahaan(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'profilperusahaan'
    model = models.company
    model = models.users
    template_name = 'profile.html'

class ListKaryawan(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'listkaryawans'
    model = models.users
    template_name = 'karyawan_list.html'

class DetailKaryawan(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = models.users
    template_name = 'karyawan_detail.html'

class ListKaryawanDeleteView(LoginRequiredMixin,DeleteView):
    context_object_name = 'listkaryawans'
    model = models.users
    template_name = 'karyawan_confirm_delete.html'
    success_url = reverse_lazy('listkaryawan')

class ListKaryawanUpdateView(LoginRequiredMixin,UpdateView):
    fields = ('name','telp')
    model = models.users
    template_name = 'karyawan_update.html'
    success_url = reverse_lazy('listkaryawan')

class ListVacation(LoginRequiredMixin,ListView):
    context_object_name = 'listvacations'
    model = models.vacation
    template_name = 'vacation_list.html'
