from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Question(models.Model):
    content = RichTextField()
    solution = RichTextField()
    answer = RichTextField(default="Test")
    def __str__(self):
        return u'%s. %s' %(self.id,self.content)