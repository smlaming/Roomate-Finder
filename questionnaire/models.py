from django import forms
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

import re
from django.core.exceptions import ValidationError
from datetime import date


# Create your models here.
'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text


class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)


class PersonalityForm(forms.Form):
    name = forms.CharField(label='Your name: ', max_length=200)
    #year = forms.MultipleChoiceField(label="Year: ", choices=(('1', '1st'), ('2','2nd'), ('3','3rd'), ('4', '4th')))

'''

class Question(models.Model):
    user = models.OneToOneField(User, null =True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    year = models.CharField(max_length=50, choices=(('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th')))
    wake_up = models.CharField(max_length=200, choices=(('1', 'Before 7am'), ('2', '7am-8:30am'), ('3', '8:30am-10am'), ('4', '10am-11:30am'), ('5', 'After 11:30am')))
    go_to_bed = models.CharField(max_length=200, choices=(('1', 'Before 9pm'), ('2', '9pm-10:30pm'), ('3', '10:30pm-12:00am'), ('4', '12:00am-1:30am'), ('5', 'After 1:30am')))
    how_clean = models.CharField(max_length=200, choices=(('1', 'Very Clean'), ('2', 'Kinda Clean'), ('3', 'Kinda Messy'), ('4', 'Very Messy')))
    guests = models.CharField(max_length=200, choices=(('1', 'Always love to have guests over'), ('2', 'Usually love to have guests over'), ('3', 'Sometimes love to have guests over'), ('4', 'Never love to have guests over')))
    more_introverted_or_extroverted = models.CharField(max_length=200, choices=(('1', 'Introverted'), ('2', 'Extroverted'), ('3', 'In the middle')))
    ideal_rent = models.PositiveBigIntegerField()
    pfp = models.ImageField(null=True, blank=True) #text field that's a path to an image, rather than save in the form, save as a form of media
    bio = models.TextField(null=True)
    # profile_pic = models.ImageField(upload_to=...)

    def __str__(self):
        return str(self.user)

    def get_user(self): # received help from Jude in OH to create this function / use it in views
        return self.user


    def check_rent(self):
        rentNum = self.cleaned_data['ideal_rent']
        if rentNum < 100:
            raise ValidationError("rent too low!")

        return rentNum

#https://georgexyz.com/django-model-form-validation.html
def day_validator(value):
    #if not isinstance(value, int):

    month = str(value.month)
    day = str(value.day)
    if len(month) < 2:
        month = "0"+month
    if len(day) < 2:
        day = "0"+day
    value_as_str = str(value.year)+"-"+str(month)+"-"+str(day)
    today = date.today()
    # https://stackoverflow.com/questions/14225608/python-how-to-use-regex-in-an-if-statement
    '''
    if not re.match(regex, value):
        raise ValidationError(
            ('%(value)s not a properly formatted date: please use YYYY-MM-DD'),
            params={'value':value}
        )
    '''
    #https://www.geeksforgeeks.org/python-program-to-print-current-year-month-and-day/#:~:text=In%20Python%2C%20in%20order%20to%20print%20the%20current,function%20of%20date%20class%20to%20fetch%20todays%20date.
    #https://izziswift.com/how-do-i-validate-a-date-string-format-in-python/
    if (int(value_as_str[0:4]) < int(today.year)):
        raise ValidationError(
            ('%(value)s not a valid year: please use this year or an upcoming year'),
            params={'value':value}
        )
    elif (int(value_as_str[0:4]) == int(today.year)) and (int(value_as_str[5:7])< int(today.month)):
        raise ValidationError(
            ('%(value)s not a valid month: please use a month that has not already passed'),
            params={'value':value}
        )
    elif (int(value_as_str[5:7]) == int(today.month)) and (int(value_as_str[8:10]) < int(today.day)):
        raise ValidationError(
            ('%(value)s not a valid day: please use a day that has not passed yet'),
            params={'value':value}
        )


def time_validator(value):
    #regex = '[0-9][0-9]:[0-9][0-9]'
    hour = str(value.hour)
    min = str(value.min)[0:2]
    '''
    if len(hour) < 2:
        hour = "0" + hour
    if len(min) < 2:
        min = "0" + min
    '''
    if int(hour) < 0 or int(hour) > 23:
        raise ValidationError(
            ('%(value)s not a proper hour: please enter a valid hour'),
            params={'value':value}
        )
    elif int(min) < 0 or int(min) > 59:
        raise ValidationError(
            ('%(value)s not a proper minute: please enter a proper minute value'),
            params={'value':value}
        )

class Event(models.Model):
    summary = models.CharField(max_length=200)
    zoom_link = models.URLField(max_length=200, blank=True)
    day = models.DateField(auto_now=False, help_text='YYYY-MM-DD', validators=[day_validator]) #YYYY-MM-DD HH:MM #
    start_time = models.TimeField(auto_now=False, help_text='HH:MM', validators=[time_validator])
    duration = models.IntegerField(default=1)
    inviter = models.EmailField()
    invitee = models.EmailField()

    def __str__(self):
        return self.summary

