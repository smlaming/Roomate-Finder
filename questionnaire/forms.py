from django import forms
from .models import Question, Event

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('user', 'name', 'email', 'year', 'wake_up', 'go_to_bed', 'how_clean', 'guests', 'more_introverted_or_extroverted', 'ideal_rent', 'pfp', 'bio')
        exclude = ('user',)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('summary', 'zoom_link', 'day', 'start_time', 'duration', 'inviter', 'invitee')
        exclude = ('inviter', 'invitee',)
        #widgets = {name of field :
        # {day : forms.DateInput(**edit attributes**)}
        #import scrips into html (JQuery Date Picker) possibly
        #received help from Daniel Zhao in OH
        #https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#dateinput
        #https://stackoverflow.com/questions/59035021/django-dateinput-widget-not-working-in-modelform
        widgets = {
            'day': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'start_time':forms.TimeInput(attrs={'class':'form-control', 'type':'time'})
        }
