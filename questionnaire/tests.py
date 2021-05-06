from django.test import TestCase
from django.test import SimpleTestCase
from questionnaire.models import Question
from questionnaire.forms import QuestionForm
from django.urls import reverse, resolve
from django.test import Client
from questionnaire.views import index, answers, user_profile
from questionnaire.urls import urlpatterns

class Tests(TestCase):

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

	def test_blank_name_form7(self):
		form_data = {'name':'','email':'test@virginia.edu','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
				 'more_introverted_or_extroverted':'1','ideal_rent':'1000','bio':'hi'}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())

	def test_blank_rent_form8(self):
		form_data = {'name':'test','email':'test@virginia.edu','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
		'more_introverted_or_extroverted':'1','ideal_rent':'','bio':'hi'}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())

	def test_blank_email_form9(self):
		form_data = {'name':'test','email':'','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
				 'more_introverted_or_extroverted':'1','ideal_rent':'','bio':'hi'}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())


	def test_low_rent(self):
		form_data = {'name':'test','email':'test@virginia.edu','year':'1','wake_up':'1','go_to_bed':'1','how_clean':'1','guests':'1',
				 'more_introverted_or_extroverted':'1','ideal_rent':'50','bio':'hi'}
		form = QuestionForm(data=form_data)
		self.assertFalse(form.is_valid())

	def test_email(self):
		form = self.create_form()
		label = form._meta.get_field('email').verbose_name
		self.assertEqual(label, 'email')

	def test_name(self):
		form = self.create_form()
		label = form._meta.get_field('name').verbose_name
		self.assertEqual(label, 'name')

	def test_bio(self):
		form = self.create_form()
		label = form._meta.get_field('bio').verbose_name
		self.assertEqual(label, 'bio')

	def test_ideal_rent(self):
		form = self.create_form()
		label = form._meta.get_field('ideal_rent').verbose_name
		self.assertEqual(label, 'ideal rent')

	def test_max_length_name(self):
		form = self.create_form()
		max_length = form._meta.get_field('name').max_length
		self.assertEqual(max_length, 100)

	def test_user_test(self):
		form = self.create_form()
		self.assertEqual(form.get_user(), None)

	def test_user_test2(self):
		form = self.create_form()
		self.assertEqual(form.__str__(), 'None')

	def test_form_inputs(self):
		form = self.create_form()
		expected = f'{form.name}, {form.email}'
		self.assertEqual(expected, 'test, test@virginia.edu')

