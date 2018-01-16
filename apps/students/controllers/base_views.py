from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from webmodels.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
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
        if (request.user.is_authenticated):
            return redirect('/students/home')
        else:
            return LoginView.as_view()(request)

    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            # save user
            if form.is_valid():
                user = form.save()
                messages.add_message(request, messages.SUCCESS, "User created successfully, Please Login")
                # TODO : does user needs to be superuser/staff
                user_permission = UserPermission(owner=user, is_teacher=False)
                user_permission.save()
                return redirect('/students/login')
        else:
            form = UserCreationForm()

        param ={'form': form}
        return render(request,'registration/register.html',param)

    def log_out(request):
        param ={}
        #return logout_then_login(request, login_url ='/students/login')
        logout(request)
        return redirect('/students/login')
