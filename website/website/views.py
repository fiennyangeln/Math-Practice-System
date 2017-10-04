from django.http import HttpResponse
from django.template.loader import get_template


def homepage(request):
   t=get_template('homepage/index.html')
   html = t.render()
   return HttpResponse(html)

def show_question(request):
   t=get_template('show_q.html')
   html = t.render()
   return HttpResponse(html)


