from django.conf.urls import url,include
from .controllers.base_views import BaseView
from .controllers.concept_views import ConceptView
from .controllers.search_views import SearchView
from .controllers.exercise_views import ExerciseView
from .controllers.practice_views import PracticeView
from .controllers.quiz_views import QuizView
from .controllers.paper_views import PaperView

urlpatterns = [
    url(r'^$', BaseView.log_in, name="default"),
    url(r'^login/$',BaseView.log_in, name="students_login"),
    url(r'^logout/$',BaseView.log_out, name="students_logout"),
    url (r'^register/$',BaseView.register,name="students_register"),
    url(r'^home/$', BaseView.dashboard, name="students_home"),
    url(r'^switch_edu/(?P<edu_id>[0-9]+)/$', BaseView.switch_edu, name="students_switchedu"),
    url(r'^switch_edu/$', BaseView.switch_edu, name="students_switchedu"),
    url(r'^concepts/$', ConceptView.dashboard, name="students_concept"),
    url(r'^search/$', SearchView.dashboard, name ="students_search"),
    url(r'^exercise/$', ExerciseView.dashboard, name ="students_exercise"),
    url(r'^practice/$', PracticeView.dashboard, name="students_practice"),
    url(r'^qa/$', BaseView.qa, name="students_qa"),
    url(r'^paper/$', PaperView.dashboard, name ="students_paper"),
    url(r'^quiz/$', QuizView.dashboard, name="students_quiz"),

]
