from django import forms
from django.forms import Form, ModelForm, fields
from schema.models import deliverables_db
from schema.models import rubrics_evaluation_db

class rubrics_evaluation_dbform(ModelForm):
    
    class Meta:
        model = rubrics_evaluation_db
        fields= ['usn','prof','rubrics','r_marks_obtained']
        unique_together = [['usn', 'prof','rubrics']]
        
        #display phse id and usn
    def save(self, commit=True):
        deliverable = super().save(commit=False)
        if commit:
            deliverable.save()
        return deliverable
