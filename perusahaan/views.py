from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (View,TemplateView,ListView,DetailView,
                                CreateView,UpdateView,
                                DeleteView)
from perusahaan import models

# Create your views here.

class IndexPerusahaan(ListView):
    model = models.company
    template_name = 'index.html'
class BuatDataPerusahaan(CreateView):
    model = models.company
    fields = ('name','address','email','telp','location')
    template_name = 'perusahaan_form.html'
    success_url = reverse_lazy('index')
