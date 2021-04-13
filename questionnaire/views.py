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
        form = QuestionForm(request.POST, request.FILES)
        names = request.user.username

        if form.is_valid():
            answers = form.save(commit=False)
            answers.user = request.user
            answers.save()
 
    form = QuestionForm()  # bound form
    return render(request, 'form.html', {'form': form})


def match(username1, username2):
    user1 = Question.objects.get(user=username1)
    user2 = Question.objects.get(user=username2)
    match_num = 0
    if user1.year == user2.year:
        match_num += 1
    if user1.wake_up == user2.wake_up:
        match_num += 1
    if user1.go_to_bed == user2.go_to_bed:
        match_num += 1
    if user1.how_clean == user2.how_clean:
        match_num += 1
    if user1.guests == user2.guests:
        match_num += 1
    if user1.more_introverted_or_extroverted == user2.more_introverted_or_extroverted:
        match_num += 1
    if user2.ideal_rent - 100 >= user1.ideal_rent >= user2.ideal_rent + 100:
        match_num += 1
    return match_num

def answers(request, username):
    all_users = Question.objects.all()
    curr_user = User.objects.get(username=username)
    matches = []
    for user in all_users:
        if user.get_user() != curr_user:
            match_score = match(curr_user, user.get_user())
            if match_score >= 4:
                matches.append(user)
    context = {
        "all_users": all_users,
        "curr_user": curr_user,
        "matches": matches
    }
    return render(request, 'answers.html', context)


def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        "user": user
    }

    return render(request, 'user_profile.html')
