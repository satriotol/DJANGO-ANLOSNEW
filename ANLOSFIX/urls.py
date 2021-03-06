"""ANLOSFIX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from perusahaan import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'presence', main_views.PresenceViewSet),
router.register(r'upload', main_views.UploadFaceView),
router.register(r'vacation', main_views.VacationViewSet),

urlpatterns = [
    # password reset

    # api
    path('api/',include(router.urls)),
    path('api/location/',main_views.record_location_list),
    path('api/location/<int:pk>',main_views.record_location_detail, name='record_location_detail'),
    path('api/login/',main_views.UserListView),
    # url
    path('admin/', admin.site.urls),
    path('',main_views.IndexPerusahaan.as_view(),name='index'),
    path('pengaturan/<int:pk>/',main_views.EditUser.as_view(),name='edituser'),
    path('pengaturan/lokasi/<int:pk>/',main_views.EditLocation.as_view(),name='editlocation'),
    path('pengaturan/karyawan/<int:pk>/',main_views.EditKaryawan.as_view(),name='editkaryawan'),
    path('register/',main_views.registercompany,name='create'),
    path('registerkaryawan/',main_views.registeruser,name='create_karyawan'),
    path('record_location/',main_views.record_location,name='record_location'),
    path('delete/<int:pk>/',main_views.ListKaryawanDeleteView.as_view(),name="delete"),
    path('<int:pk>/update/',main_views.ListKaryawanUpdateView.as_view(),name='update'),
    path('list/',main_views.ListKaryawan.as_view(),name='listkaryawan'),
    path('list/<int:pk>/',main_views.DetailKaryawan.as_view(),name='detail'),
    path('profile/<int:pk>',main_views.ProfilePerusahaan.as_view(),name='profile_perusahaan'),

    # presence
    path("presence/",main_views.RekapPresensiList.as_view(), name="presence"),
    path("presence/<int:pk>",main_views.RekapPresensiDelete.as_view(), name="presence_delete"),
    path("api/p/",main_views.userPresence, name="p"),

    # cuti
    path("cuti/",main_views.ListVacation.as_view(),name="cuti_pending"),
    path("cuti/acc",main_views.ListVacationAccepted.as_view(),name="cuti_acc"),
    path("cuti/rejected",main_views.ListVacationRejected.as_view(),name="cuti_rejected"),
    # path("cuti/<int:pk>/",main_views.UpdateVacation.as_view(),name="update_cuti"),
    path("cuti/<int:id>/",main_views.UpdateVacationNew,name="update_cuti"),


    # auth
    path("forget/",include('django.contrib.auth.urls')),
    path('login/',main_views.user_login,name='user_login'),
    path('logout/',main_views.user_logout,name='logout'),


    path("upload/",main_views.ImageFieldView.as_view(),name='upload'),
    path("upload/<int:pk>",main_views.ImageFieldUpdate.as_view(),name='upload_update'),

    #face_recognition
    path("api/facerecognition/",main_views.prediksiWajah),

    path("password/", main_views.change_password,name="change_password"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

