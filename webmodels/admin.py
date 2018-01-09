from django.contrib import admin
from .models import *
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')
    class Media:
        js = ('ckeditor.js',)

admin.site.register(Question,QuestionAdmin)

class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(EducationLevel,EducationLevelAdmin)
