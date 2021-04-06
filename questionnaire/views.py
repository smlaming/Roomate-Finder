from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


from .forms import QuestionForm
from .models import Question

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
        names = request.user.username

        if form.is_valid():
            answers = form.save(commit=False)
            answers.user = request.user
            answers.save()
 
    form = QuestionForm()  # bound form
    return render(request, 'form.html', {'form': form})


def answers(request):
    return render(request, 'answers.html')


def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        "user": user
    }

    return render(request, 'user_profile.html')