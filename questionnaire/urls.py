from django.urls import path

from . import views

app_name = 'questionnaire'
urlpatterns = [
    path('', views.index, name='index'),
    path('answers/', views.answers, name='answers'),
]