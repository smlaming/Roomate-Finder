from django import forms
from .models import Question, Event

class QuestionForm(forms.ModelForm):
    '''
        / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
            *REFERENCES
            *Title: Creating forms from models
            *Author: Django
            *Date: N/A
            *Code version: Python
            *URL: https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
            *Software License: BSD-3
            *Used for: Creating model forms
        '''
    class Meta:
        model = Question
        fields = ('user', 'name', 'email', 'year', 'wake_up', 'go_to_bed', 'how_clean', 'guests', 'more_introverted_or_extroverted', 'ideal_rent', 'pfp', 'bio')
        exclude = ('user',)

class EventForm(forms.ModelForm):
    '''
    / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
        *REFERENCES
        *Title: DateInput/TimeInput
        *Author: Django
        *Date: N/A
        *Code version: Python
        *URL: https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#dateinput
        *Software License: BSD-3
        *Used for: Formatting the 'day' and 'start_time' variables as widgets
        *
        *Title: Django DateInput() widget not working in ModelForm
        *Author: ArthurEzenwanne
        *Date: N/A
        *Code version: Python
        *URL: https://stackoverflow.com/questions/59035021/django-dateinput-widget-not-working-in-modelform
        *Software License: N/A
        *Used for: Debugging the widgets (assigning proper attrs)
        *
    '''
    class Meta:
        model = Event
        fields = ('summary', 'zoom_link', 'day', 'start_time', 'duration', 'inviter', 'invitee')
        exclude = ('inviter', 'invitee',)
        #received help from Daniel Zhao in OH
        widgets = {
            'day': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'start_time':forms.TimeInput(attrs={'class':'form-control', 'type':'time'})
        }
