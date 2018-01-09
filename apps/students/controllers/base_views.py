from django.shortcuts import render
from django.http import HttpResponseRedirect
from webmodels.models import *
class BaseView():
    def dashboard(request):
        param={'edu_level':EducationLevel.objects.all()}
        print (request.session.get('edu_id'))
        return render(request,'index.html',param)

    def switch_edu(request, edu_id):
        if (edu_id!=0):
            request.session['edu_id'] = edu_id
            print (request.session.get('edu_id'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
