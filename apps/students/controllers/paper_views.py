from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from webmodels.models import *
from apps.students.decorators import *
from apps.students.forms import PaperCreationForm
from apps.commons.retrievers import *
class PaperView():

    @edu_level_selected
    def dashboard(request):
        param={'paper_tests':PaperTest.objects.all()}
        return render(request,'paper/index.html',param)

    @edu_level_selected
    def create_paper(request):
        topics = get_topics(request)
        if request.method == 'POST':
            form = PaperCreationForm(request.POST)
            print(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                paper_test = PaperTest( name=data['name'],
                                        total_completion_time=data['total_completion_time'],
                                        user=request.user,
                                        difficulty_degree=data['difficulty_degree'])
                messages.add_message(request, messages.SUCCESS, "Papertest created successfully")
                paper_test.save()
                number_of_questions = 0
                average_difficulty_degree = 0
                total_marks = 0
                for topic in topics:
                    if ('topic_' + str(topic.id) + '_cb' in request.POST and
                       'topic_' + str(topic.id) + '_num' in request.POST):
                        if request.POST['topic_' + str(topic.id) + '_cb'] == 'on':
                            # Get questions based on topic
                            num_questions = request.POST['topic_' +
                                                         str(topic.id) + '_num']
                            concepts = Concept.objects.filter(topic=topic)

                            questions = retrieve_questions(
                                concepts,
                                paper_test.difficulty_degree,
                                int(num_questions))

                            # Assign these questions to the paper test
                            for question in questions:
                                paper_test.questions.add(question)
                                number_of_questions = number_of_questions + 1
                                average_difficulty_degree += (
                                    question.float_difficulty_level)
                                total_marks += question.mark
                paper_test.mark = total_marks
                paper_test.number_of_questions = number_of_questions
                if (number_of_questions!=0):
                    average_difficulty_degree = average_difficulty_degree/number_of_questions
                paper_test.average_difficulty_degree = round(average_difficulty_degree, 2)
                paper_test.save()

                return redirect('/students/paper/')


        form = PaperCreationForm()
        param = {'form':form, 'topics': topics}
        return render(request,'paper/create.html',param)

    @edu_level_selected
    def specific_paper(request, paper_test_id):
        # because django does not provide delete 
        if request.method == 'POST':
            PaperTest.objects.filter(pk=paper_test_id).delete()
            messages.add_message(request,messages.SUCCESS,"PaperTest deleted successfully")
            return redirect('/students/paper/')

        paper_test = PaperTest.objects.get(pk=paper_test_id)
        questions = paper_test.questions.all()
        param = {'paper_test': paper_test, 'questions': questions}
        return render(request,'paper/try.html',param)
