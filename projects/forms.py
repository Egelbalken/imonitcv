from django.forms import ModelForm
from django import forms
from .models import Project,Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description',
         'demo_link','source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kvargs):
        super(ProjectForm, self).__init__(*args, **kvargs)

        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class':'input'})
        
        #self.fields['title'].widget.attrs.update({'class':'input', 'placeholder': 'Add title'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'valu': 'Place your vote',
            'body': 'Add a comment with your vote.'
        }

    def __init__(self, *args, **kvargs):
        super(ReviewForm, self).__init__(*args, **kvargs)

        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class':'input'})