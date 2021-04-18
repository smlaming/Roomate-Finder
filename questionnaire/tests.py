from django.test import TestCase
from django.test import SimpleTestCase
from questionnaire.models import Question
from questionnaire.forms import QuestionForm
from django.urls import reverse, resolve
from django.test import Client
from questionnaire.views import index, answers, user_profile
from django.urls import *

class Tests(TestCase):

# Form Test
	def create_form(self):
		return Question.objects.create(name='test', email='test@virginia.edu', year='1',wake_up='1',go_to_bed='1',how_clean='1',guests='1',
			more_introverted_or_extroverted='1',ideal_rent=500, bio='hi' )

	def test_is_form(self):
		form = self.create_form()
		self.assertTrue(isinstance(form, Question))

	def test_weird_fields_form2(self):
		form_data = {'pizza':'hi','name':'John'}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())

	def test_valid_form_form3(self):
		form_data = {'name':'test','email':'test@virginia.edu','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
		'more_introverted_or_extroverted':'1','ideal_rent':500,'bio':'hi'}
		form = QuestionForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_bad_rent_form4(self):
		form_data = {'name':'test','email':'test@virginia.edu','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
		'more_introverted_or_extroverted':'1','ideal_rent':'notanumber','bio':'hi'}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())

	def test_bad_email_form5(self):
		form_data = {'name':'test','email':'notagoodemail','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
		'more_introverted_or_extroverted':'1','ideal_rent':'notanumber','bio':'hi'}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())

	def test_blank_bio_form6(self):
		form_data = {'name':'test','email':'test@virginia.edu','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
		'more_introverted_or_extroverted':'1','ideal_rent':'notanumber','bio':''}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())


# Views Test
	def test_home_view(self):
		client = Client()
		response = client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)