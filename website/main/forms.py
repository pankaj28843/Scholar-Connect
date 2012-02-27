from django import forms
from main.models import *

class ProfessorSearchForm(forms.Form):
    confrence = forms.ModelChoiceField(queryset = Confrence.objects.all().order_by('name', '-year'), label="Which Conference")
    professor = forms.ModelChoiceField(queryset = Professor.objects.all().order_by('name'), label="Who are you")
    
class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
