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
    This function renders and saves the "roommate questionnaire" form
    '''
    '''/ ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
        *REFERENCES
        *Title: Retrieving Objects
        *Author: Django
        *Date: N/A
        *Code version: Python
        *URL: https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-specific-objects-with-filters
        *Software License: BSD-3
        *Used for: Retrieiving the current users "Question" object
        *
        *Title: Save form data in Django
        *Author: 'Rohan'
        *Date: Sept. 6 2015
        *Code version: Python
        *URL: https://stackoverflow.com/questions/32423401/save-form-data-in-django
        *Software License: N/A
        *Used for: Saving form info
        *
        *Title: HTTP redirect
        *Author: Django
        *Date: N/A
        *Code version: Python
        *URL: https://docs.djangoproject.com/en/dev/topics/http/urls/#reverse
        *Software License: BSD-3
        *Used for: response redirect to profile page
        *
        ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /'''
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        names = request.user.username
        if form.is_valid():
            #received help from Sam McBroom in OH to figure out how to resolve overwriting existing entries
            try:
                curr_user = Question.objects.get(user=request.user)
            except (KeyError, Question.DoesNotExist):
                form_answers = form.save(commit=False)
                form_answers.user = request.user
            #Quesiton.objects.get(user=request.user)
            #if record exists, instead of saving just change the fields
            #current record = , then update each individual field (if it changed, then update)
                form_answers.save() #if form doesn't already exist

            else: #overwrites existing answers with the user's new response
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
                curr_user.save()
            # redirect to the user's profile page
            return HttpResponseRedirect(reverse('questionnaire:profile', args=(names,)))
 
    form = QuestionForm()  # bound form
    return render(request, 'form.html', {'form': form})


def match(username1, username2):
    '''
    :param username1: username of potential match
    :param username2: username of potential match
    :return: an int representing the number of answer matches that the two given users have
    '''
    # get both users information
    user1 = Question.objects.get(user=username1)
    user2 = Question.objects.get(user=username2)
    match_num = 0
    #compare on each form input
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
    '''
    :param request
    :param username: current user's username
    This function renders the information used to calculate the "your results" page
    '''
    '''/ ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    *REFERENCES
    *Title: How to Create Dynamic URLs in Django
    *Author: Learning about Electronics
    *Date: N/A
    *Code version: Python/HTML
    *URL: http://www.learningaboutelectronics.com/Articles/How-to-create-dynamic-URLs-in-Django.php
    *Software License: N/A
    *Used for: rendering the 'create event' url button in answers.html
    *
    '''
    try:
        all_users = Question.objects.all()
        curr_user = User.objects.get(username=username)
        matches = []
        # look through each user in the database and see if they match on 4 or more items, if so, they're a 'match'
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
    except: #if the user hasn't submitted the questionnaire yet, this except clause will kick in
        curr_user = User.objects.get(username=username)
        context = {
            "all_users": None,
            "curr_user": curr_user,
            "matches": [],
            'username': username
        }
    return render(request, 'answers.html', context)


def user_profile(request, username):
    '''
    :param request:
    :param username: the current users username
    renders information for the users profile
    '''
    try:
        user_obj = User.objects.get(username=username)
        question_obj = Question.objects.get(user=user_obj)
        context = {
            "user": user_obj,
            "responses": question_obj,
            "username":username
        }
    except: #if the user has not submitted a questionnaire yet
        user_obj = User.objects.get(username=username)
        context = {
            'user': user_obj,
            'responses': None,
            'username': username
        }

    return render(request, 'user_profile.html', context)


def calendar(request, username):
    '''
    this function integrates the calendar API, makes the current user a reader of the "project A22" calendar, and lists the
    events that they currently have planned with their potential matches
    '''
    '''/ ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    *REFERENCES
    *Title: Integrating Google Calendar API into Python Projects
    *Author: nikhil kumarsingh
    *Date: May 10, 2019
    *Code version: Python
    *URL: https://www.youtube.com/watch?v=j1mh0or2CX8
    *URL: https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322
    *Software License: N/A
    *Used for: Followed this Youtube video to get the basics of the Google Calendar API integration as well as the
    basics of the 'create_event()' function
    *
    *Title: Python Quickstart
    *Author: Google
    *Date: N/A
    *Code version: Python
    *URL: https://developers.google.com/calendar/quickstart/python
    *Software License: Apache 2.0
    *Used for: Used the sample code to get the base of the Calendar API integration
    *
    *Title: Acl
    *Author: Google
    *Date: N/A
    *Code version: Python
    *URL: https://developers.google.com/calendar/v3/reference/acl
    *Software License: Apache 2.0
    *Used for: Granting users access to read the project admin calendar so that they can view their events 
    *
    *Title: CalendarList: list
    *Author: Google
    *Date: N/A
    *Code version: Python
    *URL: https://developers.google.com/calendar/v3/reference/calendarList/list
    *Software License: Apache 2.0
    *Used for: Accessing just the "roommate finder calendar" ID from the project admin account  
    *
    ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /'''
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time. <- from the Google API calendar starter
    #lines 221-238 are from the Google quickstart
    if os.path.exists('questionnaire/token.json'):
        creds = Credentials.from_authorized_user_file('questionnaire/token.json', SCOPES) #the creds in token.json are for the project admin calendar
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
        roommate_cal_ID = created_cal['id'] # grab the ID of the calendar

    #grant user permission to read the admin calendar
    rule = {
        'scope': {
            'type' : 'user',
            'value' : request.user.email
        },
        'role' : 'reader'
    }
    cal_acl = service.acl().list(calendarId=roommate_cal_ID).execute()
    is_a_reader = False
    #see if the person is already a reader
    for r in cal_acl['items']:
        if r['scope']['value'] == request.user.email:
            is_a_reader = True
    #if the person is not already a reader, make them a reader of the calendar
    if not is_a_reader:
        created_rule = service.acl().insert(calendarId=roommate_cal_ID, body=rule).execute()

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # result = service.calendarList().list().execute() - list of calendars,
    events_result = service.events().list(calendarId=roommate_cal_ID, timeMin=now, singleEvents=True,
                                          orderBy='startTime').execute()
    # service.calendarList().list().execute() - outputs all calendars

    # only list events where the current user is an attendee
    events = events_result.get('items', [])
    my_events = []
    for e in events:
        for email in e['attendees']:
            if email['email'] == request.user.email:
                my_events.append(e)

    context = {
        'events': my_events
    }
    return render(request, 'calendar.html', context)

def make_event(day, start_time, summary, user_email1, user_email2, duration=1, description=None, location=None):
    '''
    :param day: Date of the event
    :param start_time: Start time of the event
    :param summary: Description of the event
    :param user_email1: email of one attendee
    :param user_email2: email of the other attendee
    :param duration: length of meeting
    :param description: defauly var
    :param location: default var
    :return: a dictionary formatted to be created as a Google Calendar event
    '''
    '''/ ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
    *REFERENCES
    *Title: Integrating Google Calendar API into Python Projects
    *Author: nikhil kumarsingh
    *Date: May 10, 2019
    *Code version: Python
    *URL: https://www.youtube.com/watch?v=j1mh0or2CX8
    *URL: https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322
    *Software License: N/A
    *Used for: Followed this Youtube video to get the basics of the Google Calendar API integration as well as the
    basics of the 'create_event()' function
    *
    *Title: Events
    *Author: Google
    *Date: N/A
    *Code version: Python
    *URL: https://developers.google.com/calendar/v3/reference/events
    *Software License: Apache 2.0
    *Used for: understanding event dictionary keys / formatting event dictionary   
    *
    '''
    #format hours and dates properly
    start_hour = str(start_time)[0:2]
    start_min = str(start_time)[2:]
    end_hour = str(int(start_hour)+duration)
    if len(str(end_hour)) < 2: # format hours less than 10 with a 0 before the number
        end_hour = str(0) + end_hour
    #'2015-05-28T09:00:00-07:00' <- format of time/date
    start_time = str(day) + "T" + str(start_hour) + start_min
    end_time = str(day) + "T" + str(end_hour) + start_min
    #end_time = start_time + timedelta(hours=duration)
    # populate event dictionary with provided information
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
        'organizer' : {
            'email':user_email1
        },
        'visibility': 'private',
        'attendees': [
            {'email': user_email1},
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
    return event

def create_event(request, username):
    '''
    This function renders the information for the 'create event' form and sets up calendar permissions
    '''
    '''/ ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
        *REFERENCES
        *Title: Integrating Google Calendar API into Python Projects
        *Author: nikhil kumarsingh
        *Date: May 10, 2019
        *Code version: Python
        *URL: https://www.youtube.com/watch?v=j1mh0or2CX8
        *URL: https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322
        *Software License: N/A
        *Used for: Followed this Youtube video to get the basics of the Google Calendar API integration as well as the
        basics of the 'create_event()' function
        *
        *Title: Python Quickstart
        *Author: Google
        *Date: N/A
        *Code version: Python
        *URL: https://developers.google.com/calendar/quickstart/python
        *Software License: Apache 2.0
        *Used for: Used the sample code to get the base of the Calendar API integration
        *
        *Title: CalendarList: list
        *Author: Google
        *Date: N/A
        *Code version: Python
        *URL: https://developers.google.com/calendar/v3/reference/calendarList/list
        *Software License: Apache 2.0
        *Used for: Accessing just the "roommate finder calendar" ID from the project admin account  
        *
    *Title: Events
    *Author: Google
    *Date: N/A
    *Code version: Python
    *URL: https://developers.google.com/calendar/v3/reference/events
    *Software License: Apache 2.0
    *Used for: inserting the new event and accessing information from it   
    *
        ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /'''
    match = User.objects.filter(username=username)
    matches_email = match[0].email
    #get email from that match.email
    curr_user = request.user
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # lines 395-410 are from the Google quickstart
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
                roommate_cal_ID = created_cal['id'] #extract the specific ID for the admins roommate calendar

            #created_rule = service.acl().insert(calendarId=roommate_cal_ID, body=rule).execute()
            # create calendar events
            e = make_event(form_answers.day, form_answers.start_time, form_answers.summary, curr_user.email, matches_email, form_answers.duration, form_answers.zoom_link)
            event = service.events().insert(calendarId=roommate_cal_ID, body=e).execute()
            event_link = event.get('htmlLink')
            return HttpResponseRedirect(event_link) #redirect to the calendar url
            #print('Event created: %s' % (event.get('htmlLink')))

    form = EventForm()  # bound form
    return render(request, 'create_event.html', {'form': form})

