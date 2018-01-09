from django.shortcuts import render
from django.http import HttpResponseRedirect
from webmodels.models import *
class PracticeView():
    def dashboard(request):
        param={'edu_level':EducationLevel.objects.all()}
        print (request.session.get('edu_id'))
        return render(request,'index.html',param)
