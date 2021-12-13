from django import forms
from django.forms import Form, ModelForm, fields
from schema.models import deliverables_db

class DeliverablesForm(ModelForm):
    
    class Meta:
        model = deliverables_db
        fields= ['report','ppt','gdrive_link','usn','phase_id']
        unique_together = [['usn', 'phase_id']]
        
        #display phse id and usn
    def save(self, commit=True):
        deliverable = super().save(commit=False)
        if commit:
            deliverable.save()
        return deliverable

# class details(ModelForm):
