from django.shortcuts import render
from django.http import HttpResponseRedirect
from webmodels.models import *
class ExerciseView():
    def dashboard(request):
        param={'edu_level':EducationLevel.objects.all()}
        print (request.session.get('edu_id'))
        return render(request,'exercise/index.html', param)

    def try_exercise(request, question_id):
        question = Question.objects.filter(id=question_id)
        param = { 'question': question }
        return render(request, 'exercise/try.html', param)
