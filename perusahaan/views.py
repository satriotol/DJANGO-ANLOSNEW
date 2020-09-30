from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                CreateView,UpdateView,
                                DeleteView)
from perusahaan import models
from .models import users,company,ImageDatasetModel,FaceRecognitionModel, PresenceModel, VacationModel
from django.views.generic.edit import FormView
from perusahaan.forms import companyprofileform,CompanyForm,usersform,usercompanyprofileform,ImageDatasetForm, VacationForm, ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions,status,renderers,generics,filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from perusahaan.serializers import UserSerializer,UserProfileSerializer,UsersLocationSerializer,PresenceSerializer,UploadFaceSerializer, VacationSerializer
from django.core.mail import send_mail,BadHeaderError

#face recognition
import numpy as np
import os
import cv2
# end of vendor

# def sendmail(request):
#     send_mail('Halo dari anlosia',
#     'Ini Pesan Otomatis',
#     'satriotol69@gmail.com',
#     ['satriotol69@gmail.com'],
#     fail_silently=False,
#     )
#     return render(request, 'send.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

# # face recognition
# pelatihan
pengenalwajah = cv2.face.LBPHFaceRecognizer_create()
detektor = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
def perolehCitradanLabel(request):
    daftarFolderCitra = [os.path.join("media/image_field/", f)\
        for f in os.listdir("media/image_field/")]
        
    daftarSampelWajah =[]
    daftarIdWAJAH =[]
    for foldercitra in daftarFolderCitra:
        daftarBerkas = os.listdir(foldercitra)
        for berkas in daftarBerkas:
            # berkasCitra = foldercitra + "//" + berkas
            berkasCitra = foldercitra + "\\" + berkas
            print("Pemrosesan berkas citra", berkasCitra)

            citra = cv2.imread(berkasCitra, 0)

            idWajah = os.path.basename(foldercitra)
            idWajah = int(idWajah)

            daftarWajah = detektor.detectMultiScale(citra)


            for(x,y,w,h) in daftarWajah:
                daftarSampelWajah.append(
                    citra[y : y + h, x : x + w])
                daftarIdWAJAH.append(idWajah)
    return daftarSampelWajah, daftarIdWAJAH
daftarWajah, daftarIdWAJAH = perolehCitradanLabel("media/image_field")
pengenalwajah.train(daftarWajah, np.array(daftarIdWAJAH))
pengenalwajah.save(("pelatihan.yml"))

# end of pelatihan
# ================================================
# prediksi
pengenalWajah = cv2.face.LBPHFaceRecognizer_create()
detektor = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
def prediksiWajah(namaBerkas):
    face_recognition = "media/"+FaceRecognitionModel.objects.values_list("image",flat=True).order_by('-created_at')[0]
    namaBerkas = face_recognition
    citra = cv2.imread(namaBerkas)

    if citra is None:
        print("Tidak dapat membaca berkas citra")
        return

    abuAbu = cv2.cvtColor(citra, cv2.COLOR_BGR2GRAY)
    daftarwajah = detektor.detectMultiScale(
        abuAbu,scaleFactor= 1.3,minNeighbors= 5)
    if daftarwajah is None:
        print("wajah tidak terdeteksi")
        return
    for(x,y,w,h) in daftarwajah:
        cv2.rectangle(citra, (x,y),(x+w,y+h),
        (255,0,0),2)
        wajah = abuAbu[y:y+h, x:x+w]
        labelId, konfiden = pengenalWajah.predict(wajah)
        if konfiden <75:
            cv2.putText(citra,"(%s) %.0f"%
                (labelId,konfiden),
                (x,y-2),
                cv2.FONT_HERSHEY_PLAIN,
                1,(0,255,0)),
            data = ({
                "api_status" : 1,
                "message" : "sukses",
                "konfiden" : konfiden,
                "id" : labelId,
            })
        else:
            # cv2.putText(citra,"Data Tidak Terdaftar",(x,y-2),
            # cv2.FONT_HERSHEY_PLAIN,1,
            # (0,255,0))
            data = ({
                "api_status" : 0,
                "message" : "Wajah Tidak Cocok/Akurat, Coba Ulangi",
                "konfiden" : konfiden,
                "id" : labelId,
            })
        return JsonResponse(data)
    else:
        data = ({
            "api_status" : 0,
            "message" : "Data Wajah Tidak Terdaftar, Coba Ulangi"
        })
        return JsonResponse(data)

pengenalWajah.read("pelatihan.yml")
# prediksiWajah("media/image_field/9/IMG-20200907-WA0068.jpg")
# end of prediksi

# end of face recogniition

# upload face

class UploadFaceView(viewsets.ModelViewSet):
    queryset = FaceRecognitionModel.objects.all()
    serializer_class = UploadFaceSerializer


# end of upload face

# end of face recognition


        
class ImageFieldView(CreateView):
    form_class = ImageDatasetForm
    model = models.users
    context_object_name = 'listkaryawans'
    template_name = 'upload.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(ImageFieldView, self).get_context_data(**kwargs)
        context['userslist'] = users.objects.all()
        return context

class ProfileKaryawan(DetailView):
    model = models.User
    template_name = 'profile_karyawan.html'

@api_view(['POST'])
def userPresence(request):
    if request.method == 'POST':
        # presence = PresenceModel.objects.raw("SELECT * FROM perusahaan_presencemodel WHERE id_user_id = %s AND date_presence = %s AND end_presence IS NULL", [request.POST.get('id_user'), request.POST.get('date_presence')]).values('id')
        presence = PresenceModel.objects.filter(id_user_id=request.POST.get('id_user'), date_presence=request.POST.get('date_presence')).exists()
        if presence: 
            data = {}
            data['api_status'] = 0
            data["api_message"] = "Failed"
            return JsonResponse(data, safe=False)
        else :
            data = {}
            data['api_status'] = 1
            data["api_message"] = "Success"
            return JsonResponse(data, safe=False)

@api_view(['POST'])
def UserListView(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('username')).values("id","users__id_company","users__id_company__name","username","password","email","users__name","users__telp","users__profile_pic","users__id_company__location","users__id_company__start_work","users__id_company__end_work")
        if user:
            data = {}
            data['api_status'] = 1
            data['api_message'] = 'success'
            if(check_password(request.POST.get('password'),list(user)[0]["password"])):
                data['data'] = list(user)
            else:
                data['api_status'] = 0
                data["api_message"] = "Password Anda Salah"
        else:
            data = {}
            data['api_status'] = 0
            data["api_message"] = "Username Anda Tidak Ditemukan"
        return JsonResponse(data, safe=False)
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PresenceViewSet(viewsets.ModelViewSet):
    queryset = PresenceModel.objects.all()
    serializer_class = PresenceSerializer
    filter_backends = [DjangoFilterBackend,]
    filter_fields  = ["id_user",]

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

class IndexPerusahaan(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.users
    context_object_name = 'listkaryawans'
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexPerusahaan, self).get_context_data(**kwargs)
        context['presencelist'] = PresenceModel.objects.all()
        context['vacationlist'] = VacationModel.objects.all()
        return context


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

class EditUser(SuccessMessageMixin,UpdateView):
    context_object_name = 'listusers'
    model = models.company
    fields = ['name','address','start_work','end_work','profile_pic']
    template_name = 'user_update.html'
    success_url = reverse_lazy('index')
    success_message = 'List successfully saved!!!!'


class ProfilePerusahaan(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'profilperusahaan'
    model = models.company
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfilePerusahaan, self).get_context_data(**kwargs)
        context['presencelist'] = PresenceModel.objects.all()
        context['vacationlist'] = VacationModel.objects.all()
        return context

class ListKaryawan(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'listkaryawans'
    model = models.users
    template_name = 'karyawan_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListKaryawan, self).get_context_data(**kwargs)
        context['karyawanlist'] = users.objects.values_list("id_company_id",flat=True)
        return context

class DetailKaryawan(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = models.users
    template_name = 'karyawan_detail.html'

    
    def get_context_data(self, **kwargs):
        context = super(DetailKaryawan, self).get_context_data(**kwargs)
        context['userslist'] = users.objects.all()
        context['presencelist'] = PresenceModel.objects.all()
        context['vacationlist'] = VacationModel.objects.all()
        return context

class RekapPresensiList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'presences'
    model = models.PresenceModel
    template_name = 'presence_list.html'

class ListKaryawanDeleteView(LoginRequiredMixin,DeleteView):
    context_object_name = 'listkaryawans'
    model = models.User
    template_name = 'karyawan_confirm_delete.html'
    success_url = reverse_lazy('listkaryawan')

class ListKaryawanUpdateView(LoginRequiredMixin,UpdateView):
    fields = ('name','telp')
    model = models.users
    template_name = 'karyawan_update.html'
    success_url = reverse_lazy('listkaryawan')

# vacation
class ListVacation(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'vacationpendings'
    model = models.VacationModel
    template_name = 'vacation_list.html'

class ListVacationAccepted(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'vacationpendings'
    model = models.VacationModel
    template_name = 'vacation_accept.html'

class ListVacationRejected(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    context_object_name = 'vacationpendings'
    model = models.VacationModel
    template_name = 'vacation_rejected.html'

class UpdateVacation(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = models.VacationModel
    template_name = 'vacation_update.html'
    form_class = VacationForm
    success_url = reverse_lazy('cuti_pending')

def UpdateVacationNew(request,id):
    instance = get_object_or_404(VacationModel,id=id)
    form = VacationForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('cuti_pending')
    return render (request, 'vacation_update.html',{'form':form})

def UpdateVacationNew(request,id):
    instance = get_object_or_404(VacationModel,id=id)
    p_form = VacationForm(request.POST or None, instance=instance)
    form = ContactForm(request.POST)
    if form.is_valid():
        to_email = form.cleaned_data['to_email']
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
        p_form.save()
        try:
            send_mail(subject,message,from_email,[to_email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('cuti_pending')
    return render (request, 'vacation_update.html',{'p_form':p_form,'form':form,'instance':instance})

def UpdateVacationEmail(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    else:
        if request.method == 'GET':
            usersobj = users.objects.all()
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                to_email = form.cleaned_data['to_email']
                subject = form.cleaned_data['subject']
                from_email = form.cleaned_data['from_email']
                message = form.cleaned_data['message']
                try:
                    send_mail(subject,message,from_email,[to_email])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('cuti_pending')
    return render(request, "email.html", {'form': form,'usersobj':usersobj})


class VacationViewSet(viewsets.ModelViewSet):
    queryset = VacationModel.objects.all()
    serializer_class = VacationSerializer
    filter_backends = [DjangoFilterBackend,]
    filter_fields  = ["id_user",]