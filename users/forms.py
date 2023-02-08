from django.forms import forms, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name', 'email': 'Email',
        }

    def __init__(self, *args, **kvargs):
        super(CustomUserCreationForm, self).__init__(*args, **kvargs)

        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class':'input'})
        
        #self.fields['title'].widget.attrs.update({'class':'input', 'placeholder': 'Add title'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','username', 'email', 'phone', 'location', 'short_intro', 
        'bio','profile_image','social_github','social_linkedin', 'social_twitter', 
        'social_youtube', 'social_stackoverflow','social_website']

    def __init__(self, *args, **kvargs):
        super(ProfileForm, self).__init__(*args, **kvargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class':'input' })
        '''
        '''

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name','description']
        labels = '__all__'
        exclude = ['owner']

        # We dont want to include the owner field. Alt way to do it:

    def __init__(self, *args, **kvargs):
        super(SkillForm, self).__init__(*args, **kvargs)

        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class':'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        labels = '__all__'

    def __init__(self, *args, **kvargs):
        super(MessageForm, self).__init__(*args, **kvargs)

        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class':'input'})
