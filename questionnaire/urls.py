from django.urls import path

from . import views

app_name = 'questionnaire'
urlpatterns = [
    path('', views.index, name='form'),
    path('answers/<username>', views.answers, name='answers'),
    path('profile/<username>', views.user_profile, name ='profile'),

]