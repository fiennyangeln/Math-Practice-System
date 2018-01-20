from django import forms
from webmodels.constants import *
class PaperCreationForm(forms.Form):
    name = forms.CharField(label='Name', max_length=200,required= True)
    total_completion_time = forms.IntegerField(initial=60, required=True)
    difficulty_degree = forms.ChoiceField(choices=DIFFICULTIES, initial="3", required=True)
