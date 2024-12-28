from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from login import views
from django.shortcuts import render





def home(request):
    return render(request, "home.html")

def error(request):
    return render(request, "error.html")












      
       

