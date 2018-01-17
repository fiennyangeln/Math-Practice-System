from django.conf.urls import url
from .views import ApiViews
urlpatterns = [
    url(r'^check_answer/$',ApiViews.check_answer),
]
