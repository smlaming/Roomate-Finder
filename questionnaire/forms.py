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
            *
        *Title: Change label of a form field Django
        *Author: Abdul Niyas P M
        *Date: 6/18/19
        *Code version: Python
        *URL: https://stackoverflow.com/questions/56644755/change-label-of-a-form-field-django
        *Software License: N/A
        *Used for: How to add labels to questions
        '''
    class Meta:
        model = Question
        fields = ('user', 'name', 'email', 'year', 'wake_up', 'go_to_bed', 'how_clean', 'guests', 'more_introverted_or_extroverted', 'ideal_rent', 'pfp', 'bio')
        exclude = ('user',)
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'year': 'Your Year in School',
            'wake_up': 'What time do you typically wake up?',
            'go_to_bed': 'What time do you typically go to bed?',
            'how_clean': 'How clean do you like to keep your living space?',
            'guests': 'How do you feel about having guests over to your dorm/apartment/house?',
            'more_introverted_or_extroverted': 'Are you more introverted or extroverted?',
            'ideal_rent': 'What is your ideal rent payment?',
            'pfp': 'Profile Picture',
            'bio': 'Feel free to share more about yourself!'
        }
        #widgets = {
        #   'ideal_rent': forms.NumberInput(attrs={'type':'range', 'class':'slider', 'step':'50', 'min':'200', 'max':'1500','id':'rentRange',})
        #}

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
        *Title: Change label of a form field Django
        *Author: Abdul Niyas P M
        *Date: 6/18/19
        *Code version: Python
        *URL: https://stackoverflow.com/questions/56644755/change-label-of-a-form-field-django
        *Software License: N/A
        *Used for: How to add labels to questions
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
        labels = {
            'summary': 'Meeting Title',
            'zoom_link': 'Zoom Link for Meeting',
            'day': 'Day of Meeting',
            'start_time': 'Start Time of Meeting (EST)',
            'duration': 'Duration of Meeting in Hours'
        }
