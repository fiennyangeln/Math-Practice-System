from django.shortcuts import render
from django.http import HttpResponseRedirect
from webmodels.models import *
class BaseView():
    def dashboard(request):
        param={'edu_level':EducationLevel.objects.all()}
        print (type(request.session.get('edu_id')))
        return render(request,'index.html',param)

    def switch_edu(request, edu_id=0):
        if (edu_id!=0):
            request.session['edu_id'] = int(edu_id)
            print (type(request.session.get('edu_id')))
        elif 'q' in request.GET:
            request.session['edu_id'] = request.GET['q']

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def qa(request):
        return HttpResponseRedirect('http://155.69.150.211:8001/')
