from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect


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
            #received help from Sam McBroom in OH to figure out how to resolve overwriting existing entries
            #if Question.objects.get(user=request.user):
            try:
                curr_user = Question.objects.get(user=request.user)
            except (KeyError, Question.DoesNotExist): #https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-specific-objects-with-filters
                form_answers = form.save(commit=False)
                form_answers.user = request.user
            #Quesiton.objects.get(user=request.user)
            #if record exists, instead of saving just change the fields
            #current record = , then update each individual field (if it changed, then update)
            #could consider pre-filling with old info
                form_answers.save() #if form doesn't exist

            else:
                #print('here')
                #curr_user = Question.objects.get(user=request.user)
                form_answers = form.save(commit=False)
                curr_user.name = form_answers.name
                curr_user.email = form_answers.email
                curr_user.year = form_answers.year
                curr_user.wake_up = form_answers.wake_up
                curr_user.go_to_bed = form_answers.go_to_bed
                curr_user.how_clean = form_answers.how_clean
                curr_user.guests = form_answers.guests
                curr_user.more_introverted_or_extroverted = form_answers.more_introverted_or_extroverted
                curr_user.ideal_rent = form_answers.ideal_rent
                curr_user.pfp = form_answers.pfp
                curr_user.bio = form_answers.bio
                curr_user.save() #https://stackoverflow.com/questions/32423401/save-form-data-in-django

            return HttpResponseRedirect(reverse('questionnaire:profile', args=(names,))) #https://docs.djangoproject.com/en/dev/topics/http/urls/#reverse
 
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
    user_obj = User.objects.get(username=username)
    question_obj = Question.objects.get(user=user_obj)
    context = {
        "user": user_obj,
        "responses": question_obj
    }

    return render(request, 'user_profile.html', context)
