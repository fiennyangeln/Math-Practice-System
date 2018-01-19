from django.shortcuts import render
from django.http import HttpResponseRedirect
from webmodels.models import *
from apps.students.decorators import *
from apps.commons.views import *
class ExerciseView():

    @edu_level_selected
    def dashboard(request):
        edu_level = EducationLevel.objects.filter(pk=request.session['edu_id'])
        topics = Topic.objects.filter(education_level=edu_level)
        concepts = Concept.objects.filter(topic__in=topics)
        questions = Question.objects.filter(concept__in=concepts)

        param={ 'edu_level':EducationLevel.objects.all(),
                'questions': questions}

        return render(request,'exercise/index.html', param)

    @edu_level_selected
    def try_exercise(request, question_id):
        question = Question.objects.get(id=question_id)
        question = format_answer_box(question)
        param = { 'question': question }
        return render(request, 'exercise/try.html', param)
