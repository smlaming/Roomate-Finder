from django.urls import path

from . import views

app_name = 'questionnaire'
urlpatterns = [
    path('', views.index, name='form'),
    path('answers/', views.answers, name='answers'),
    path('profile/<username>', views.user_profile, name ='profile'),

]