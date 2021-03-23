from django import forms
from django.db import models

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
    name = models.CharField(max_length=100)
    email = models.EmailField()
    year = models.CharField(max_length=50, choices=(('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th')), default='1st')

    def __str__(self):
        return self.name
