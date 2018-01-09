from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Question(models.Model):
    content = RichTextField()
    solution = RichTextField()
    answer = RichTextField(default="Test")
    def __str__(self):
        return u'%s. %s' %(self.id,self.content)

class EducationLevel(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
