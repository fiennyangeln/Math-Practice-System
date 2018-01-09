from django.conf.urls import url,include
from .controllers.base_views import BaseView

urlpatterns = [
    url(r'^$', BaseView.dashboard, name="students_home"),
    url(r'^switch_edu/(?P<edu_id>[0-9]+)/$', BaseView.switch_edu, name="students_switchedu"),
]
