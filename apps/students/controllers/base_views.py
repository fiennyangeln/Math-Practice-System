from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from webmodels.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
class BaseView():
    def dashboard(request):
        param={'edu_level' : EducationLevel.objects.all()}
        return render(request,'index.html',param)

    def switch_edu(request, edu_id=0):
        if (int(edu_id)!=0):
            request.session['edu_id'] = int(edu_id)
        elif 'q' in request.GET and request.GET['q']!="0":
            request.session['edu_id'] = int(request.GET['q'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def qa(request):
        return HttpResponseRedirect('http://155.69.150.211:8001/')

    def log_in(request):
        param ={}
        if request.method == 'GET':
            if not request.user.is_authenticated:
                return redirect('/students/home')
            else:
                return render(request,'login.html',param)
        if request.method == 'POST':
            return redirect('/students/home')

    def register(request):
        param ={}
        return render(request,'register.html',param)

    def log_out(request):
        param ={}
        logout(request)
        return redirect('/students/login')
