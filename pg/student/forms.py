from django import forms
from django.forms import Form, ModelForm, fields
from schema.models import deliverables_db
from django.forms import ModelForm, TextInput
class DeliverablesForm(ModelForm):
    
    class Meta:
        model = deliverables_db
        fields= ['report','ppt','gdrive_link','usn','phase_id']
        unique_together = [['usn', 'phase_id']]
        widgets ={
            'report' : TextInput (attrs={'pattern' : "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})",
                                         'oninvalid':"this.setCustomValidity('Enter A Valid URL')",
                                          'oninput':"this.setCustomValidity('')"}),
            'ppt' : TextInput (attrs={'pattern' : "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})",
                                         'oninvalid':"this.setCustomValidity('Enter A Valid URL')",
                                          'oninput':"this.setCustomValidity('')"}),
            'gdrive_link' : TextInput (attrs={'pattern' : "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})",
                                         'oninvalid':"this.setCustomValidity('Enter A Valid URL')",
                                          'oninput':"this.setCustomValidity('')"})
            }        
        #display phse id and usn
    def save(self, commit=True):
        deliverable = super().save(commit=False)
        if commit:
            deliverable.save()
        return deliverable

# class details(ModelForm):
