from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import QuestionForm

# Create your views here.
def index(request):
    '''
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
    '''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
    form = QuestionForm()  # bound form
    return render(request, 'form.html', {'form': form})


def answers(request):
    return HttpResponse('The Results Page')
