from __future__ import print_function
import datetime
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import redirect


import os.path

#for calendar function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


from .forms import QuestionForm, EventForm
from .models import Question, Event
from .cal_setup import main as cal_main

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
        "matches": matches,
        'username':username
    }
    #http://www.learningaboutelectronics.com/Articles/How-to-create-dynamic-URLs-in-Django.php 
    return render(request, 'answers.html', context)


def user_profile(request, username):
    user_obj = User.objects.get(username=username)
    question_obj = Question.objects.get(user=user_obj)
    context = {
        "user": user_obj,
        "responses": question_obj,
        "username":username
    }

    return render(request, 'user_profile.html', context)


def calendar(request, username):
    # general set up - https://www.youtube.com/watch?v=j1mh0or2CX8
    # Calendar API - https://developers.google.com/calendar/v3/reference/calendarList/list
    # Quick Start - https://developers.google.com/calendar/quickstart/python
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('questionnaire/token.json'):
        creds = Credentials.from_authorized_user_file('questionnaire/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'questionnaire/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
            #creds = flow.run_console()
        # Save the credentials for the next run
        with open('questionnaire/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    all_calendars = service.calendarList().list().execute()
    #print(all_calendars)

    #create a 'roommate finder calendar' for the user
    roommate_cal_exists = False
    for cal in all_calendars["items"]:
        if cal.get('summary') == 'roommateFinderCalendar':
            roommate_cal_exists = True
            roommate_cal_ID = cal['id']
    if not roommate_cal_exists:
        roommate_cal = {
            'summary': 'roommateFinderCalendar',
            'timeZone': 'America/New_York'
        }
        created_cal = service.calendars().insert(body=roommate_cal).execute()
        roommate_cal_ID = created_cal['id']

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # result = service.calendarList().list().execute() - list of calendars,
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=roommate_cal_ID, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    # service.calendarList().list().execute() - outputs all calendars
    events = events_result.get('items', [])

    context = {
        'events': events
    }
    return render(request, 'calendar.html', context)

def make_event(day, start_time, summary, user_email1, user_email2, duration=1, description=None, location=None):
    start_hour = str(start_time)[0:2]
    start_min = str(start_time)[2:]
    end_hour = str(int(start_hour)+duration)
    if len(str(end_hour)) < 2:
        end_hour = str(0) + end_hour
    #'2015-05-28T09:00:00-07:00'
    start_time = str(day) + "T" + str(start_hour) + start_min
    end_time = str(day) + "T" + str(end_hour) + start_min
    #end_time = start_time + timedelta(hours=duration)
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York',
        },
        'attendees': [
            #{'email': user_email1},
            {'email': user_email2},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24*60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    #print(event)
    return event

def create_event(request, username):
    match = User.objects.filter(username=username)
    matches_email = match[0].email
    #get email from that match.email
    # to get current user call request.user
    curr_user = request.user
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('questionnaire/token.json'):
        creds = Credentials.from_authorized_user_file('questionnaire/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'questionnaire/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
            #creds = flow.run_console()
        # Save the credentials for the next run
        with open('questionnaire/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        #inviter = request.user.email

        if form.is_valid():
            form_answers = form.save(commit=False)
            #form_answers.user = request.user
            form_answers.save()

            all_calendars = service.calendarList().list().execute()
            # create a 'roommate finder calendar' for the user if it doesn't already exist
            roommate_cal_exists = False
            for cal in all_calendars["items"]:
                if cal.get('summary') == 'roommateFinderCalendar':
                    roommate_cal_exists = True
                    roommate_cal_ID = cal['id']
            if not roommate_cal_exists:
                roommate_cal = {
                    'summary': 'roommateFinderCalendar',
                    'timeZone': 'America/New_York'
                }
                created_cal = service.calendars().insert(body=roommate_cal).execute()
                roommate_cal_ID = created_cal['id']

            # create calendar events
            e = make_event(form_answers.day, form_answers.start_time, form_answers.summary, curr_user.email, matches_email, form_answers.duration, form_answers.zoom_link)
            event = service.events().insert(calendarId=roommate_cal_ID, body=e).execute()
            event_link = event.get('htmlLink')
            return HttpResponseRedirect(event_link)
            #print('Event created: %s' % (event.get('htmlLink')))

    form = EventForm()  # bound form
    return render(request, 'create_event.html', {'form': form})

