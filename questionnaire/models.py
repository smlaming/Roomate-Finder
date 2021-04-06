from django import forms
from django.db import models
from django.contrib.auth.models import User

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
username = User.get_username(User)

class Question(models.Model):
    user = models.OneToOneField(User, null =True, on_delete=models.CASCADE, default=username)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    year = models.CharField(max_length=50, choices=(('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th')))
    wake_up = models.CharField(max_length=200, choices=(('1', 'Before 7am'), ('2', '7am-8:30am'), ('3', '8:30am-10am'), ('4', '10am-11:30am'), ('5', 'After 11:30am')))
    go_to_bed = models.CharField(max_length=200, choices=(('1', 'Before 9pm'), ('2', '9pm-10:30pm'), ('3', '10:30pm-12:00am'), ('4', '12:00am-1:30am'), ('5', 'After 1:30am')))
    how_clean = models.CharField(max_length=200, choices=(('1', 'Very Clean'), ('2', 'Kinda Clean'), ('3', 'Kinda Messy'), ('4', 'Very Messy')))
    guests = models.CharField(max_length=200, choices=(('1', 'Always love to have guests over'), ('2', 'Usually love to have guests over'), ('3', 'Sometimes love to have guests over'), ('4', 'Never love to have guests over')))
    more_introverted_or_extroverted = models.CharField(max_length=200, choices=(('1', 'Introverted'), ('2', 'Extroverted'), ('3', 'In the middle')))
    ideal_rent = models.PositiveBigIntegerField()
    # profile_pic = models.ImageField(upload_to=...)


    def __str__(self):
        return self.name
