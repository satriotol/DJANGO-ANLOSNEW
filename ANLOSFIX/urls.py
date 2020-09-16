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
from django.urls import path,include
from perusahaan import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'presence', main_views.PresenceViewSet),

urlpatterns = [
    # api
    path('api/',include(router.urls)),
    path('api/location/',main_views.record_location_list),
    path('api/location/<int:pk>',main_views.record_location_detail, name='record_location_detail'),
    path('api/login/',main_views.UserListView),
    # url
    path('admin/', admin.site.urls),
    path('',main_views.IndexPerusahaan.as_view(),name='index'),
    path('pengaturan/<int:pk>/',main_views.EditUser.as_view(),name='edituser'),
    path('register/',main_views.registercompany,name='create'),
    path('registerkaryawan/',main_views.registeruser,name='create_karyawan'),
    path('profile/',main_views.ProfilePerusahaan.as_view(),name='profile'),
    path('record_location/',main_views.record_location,name='record_location'),
    path('list/',main_views.ListKaryawan.as_view(),name='listkaryawan'),
    path('delete/<int:pk>/',main_views.ListKaryawanDeleteView.as_view(),name="delete"),
    path('<int:pk>/update/',main_views.ListKaryawanUpdateView.as_view(),name='update'),
    path('vacation/',main_views.ListVacation.as_view(),name='listvacation'),
    path('list/<int:pk>/',main_views.DetailKaryawan.as_view(),name='detail'),
    path('profile/<int:pk>',main_views.ProfileKaryawan.as_view(),name='profile_karyawan'),

    # auth
    path('login/',main_views.user_login,name='user_login'),
    path('logout/',main_views.user_logout,name='logout'),

    path("upload/",main_views.ImageFieldView.as_view(),name='upload'),

    #face_recognition
    path("facerecognition/",main_views.prediksiWajah),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

