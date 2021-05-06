from django import forms
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

import re
from django.core.exceptions import ValidationError
from datetime import date


# Create your models here.

class Question(models.Model):
    '''
    / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    *REFERENCES
    *Title: Models
    *Author: Django
    *Date: N/A
    *Code version: Python
    *URL: https://docs.djangoproject.com/en/3.2/topics/db/models/
    *Software License: BSD-3
    *Used for: Creating models
    *
    *Title: Form fieldsf
    *Author: Django
    *Date: N/A
    *Code version: Python
    *URL: https://docs.djangoproject.com/en/3.2/ref/forms/fields/
    *Software License: BSD-3
    *Used for: understanding each of the fields
    *
    *Title: MaxValyeValidator, MinValueValidator
    *Author: Django
    *Date: N/A
    *Code version: Python
    *URL: https://docs.djangoproject.com/en/3.2/ref/validators/
    *Software License: BSD-3
    *Used for: understanding input checking for rent
    *
    *Title: MPython django.core.validators.MinValueValidator() Examples
    *Author: Program Creek / Yeah-Kun
    *Date: N/A
    *Code version: Python
    *URL: https://www.programcreek.com/python/example/91504/django.core.validators.MinValueValidator
    *Software License: Apache License 2.0
    *Used for: understanding how to use the Validators
    '''
    user = models.OneToOneField(User, null =True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    year = models.CharField(max_length=50, choices=(('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th')))
    wake_up = models.CharField(max_length=200, choices=(('1', 'Before 7am'), ('2', '7am-8:30am'), ('3', '8:30am-10am'), ('4', '10am-11:30am'), ('5', 'After 11:30am')))
    go_to_bed = models.CharField(max_length=200, choices=(('1', 'Before 9pm'), ('2', '9pm-10:30pm'), ('3', '10:30pm-12:00am'), ('4', '12:00am-1:30am'), ('5', 'After 1:30am')))
    how_clean = models.CharField(max_length=200, choices=(('1', 'Very Clean'), ('2', 'Kinda Clean'), ('3', 'Kinda Messy'), ('4', 'Very Messy')))
    guests = models.CharField(max_length=200, choices=(('1', 'Always love to have guests over'), ('2', 'Usually love to have guests over'), ('3', 'Sometimes love to have guests over'), ('4', 'Never love to have guests over')))
    more_introverted_or_extroverted = models.CharField(max_length=200, choices=(('1', 'Introverted'), ('2', 'Extroverted'), ('3', 'In the middle')))
    ideal_rent = models.PositiveBigIntegerField(validators=[MinValueValidator(200,message="Please enter a number above 200"), MaxValueValidator(1500, message="Please enter a number below 1500")])
    pfp = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True)
    # profile_pic = models.ImageField(upload_to=...)

    def __str__(self):
        return str(self.user)

    def get_user(self): # received help from Jude in OH to create this function / use it in views
        return self.user

    '''
    def check_rent(self):
        rentNum = self.cleaned_data['ideal_rent']
        if rentNum < 100:
            raise ValidationError("rent too low!")

        return rentNum
    '''
#https://georgexyz.com/django-model-form-validation.html
def day_validator(value):
    '''
    This function checks to see if the user tries to plan an event in a date that has already passed
    '''
    '''
    / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    *REFERENCES
    *Title: Django Model and Form Validation
    *Author: George Zhang
    *Date: 8/15/2019
    *Code version: Python
    *URL: https://georgexyz.com/django-model-form-validation.html
    *Software License: BSD-3
    *Used for: Understanding how to raise validation errors in a function 
    *
    *Title: Python program to print current year, month, and day 
    *Author: Geeks for Geeks / abhijithoyur
    *Date: 12/29/2020
    *Code version: Python3
    *URL: https://www.geeksforgeeks.org/python-program-to-print-current-year-month-and-day/#:~:text=In%20Python%2C%20in%20order%20to%20print%20the%20current,function%20of%20date%20class%20to%20fetch%20todays%20date.
    *Software License: N/A
    *Used for: how to access todays date
    '''

    # formatting the day to YYYY-MM-DD
    month = str(value.month)
    day = str(value.day)
    if len(month) < 2:
        month = "0"+month
    if len(day) < 2:
        day = "0"+day
    value_as_str = str(value.year)+"-"+str(month)+"-"+str(day)
    today = date.today()
    # compare years
    if (int(value_as_str[0:4]) < int(today.year)):
        raise ValidationError(
            ('%(value)s not a valid year: please use this year or an upcoming year'),
            params={'value':value}
        )
    #compare months
    elif (int(value_as_str[0:4]) == int(today.year)) and (int(value_as_str[5:7])< int(today.month)):
        raise ValidationError(
            ('%(value)s not a valid month: please use a month that has not already passed'),
            params={'value':value}
        )
    #compare day
    elif (int(value_as_str[5:7]) == int(today.month)) and (int(value_as_str[8:10]) < int(today.day)):
        raise ValidationError(
            ('%(value)s not a valid day: please use a day that has not passed yet'),
            params={'value':value}
        )


def time_validator(value):
    '''
    This function checks to see that the user entered a valid hour and minute for the event
    '''
    '''
        / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
        *REFERENCES
        *Title: Django Model and Form Validation
        *Author: George Zhang
        *Date: 8/15/2019
        *Code version: Python
        *URL: https://georgexyz.com/django-model-form-validation.html
        *Software License: BSD-3
        *Used for: Understanding how to raise validation errors in a function 
        *
        '''
    #format time
    hour = str(value.hour)
    min = str(value.min)[0:2]
    #check for proper hour input
    if int(hour) < 0 or int(hour) > 23:
        raise ValidationError(
            ('%(value)s not a proper hour: please enter a valid hour'),
            params={'value':value}
        )
    #check for proper minute input
    elif int(min) < 0 or int(min) > 59:
        raise ValidationError(
            ('%(value)s not a proper minute: please enter a proper minute value'),
            params={'value':value}
        )

class Event(models.Model):
    '''
        / ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
        *REFERENCES
        *Title: Models
        *Author: Django
        *Date: N/A
        *Code version: Python
        *URL: https://docs.djangoproject.com/en/3.2/topics/db/models/
        *Software License: BSD-3
        *Used for: Creating models
        *
        *Title: Form fieldsf
        *Author: Django
        *Date: N/A
        *Code version: Python
        *URL: https://docs.djangoproject.com/en/3.2/ref/forms/fields/
        *Software License: BSD-3
        *Used for: understanding each of the fields
        *
        '''
    summary = models.CharField(max_length=200)
    zoom_link = models.URLField(max_length=200, blank=True)
    day = models.DateField(auto_now=False, help_text='YYYY-MM-DD', validators=[day_validator]) #YYYY-MM-DD HH:MM #
    start_time = models.TimeField(auto_now=False, help_text='HH:MM', validators=[time_validator])
    duration = models.IntegerField(default=1)
    inviter = models.EmailField()
    invitee = models.EmailField()

    def __str__(self):
        return self.summary

