# Some standard imports here
import datetime, urllib, pdb

from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.dateparse import parse_date
from django.utils import timezone

from charterclub.models import *
from charterclub.forms import *

import charterclub
import charterclub.permissions as permissions
from charterclub.permissions import render

from events.models import Event, Entry
from events.forms import EventEntryForm, EntryDeletionForm, ChangeAnswersForm, ChangeGuestForm, ChangeRoomForm


def events_list(request):
    '''
        Show the upcoming events
    '''

    now = timezone.now()

    # Show upcoming events for the semester
    year = Student.get_senior_year()
    begin_date = now - timedelta(weeks=52)
    
    future_events = Event.objects.filter(date__gte=now).order_by("date")
    past_events = Event.objects.filter(date__gte=begin_date, date__lte=now).order_by("-date")

    # # If it is a prospective, then don't show the ones where sophomores are not allowed
    # future_events = [e for e in future_events if e.display_to_non_members]
    # past_events = [e for e in past_events if e.display_to_non_members]

    # If there is a login, setup the proper page for him
    student = permissions.get_student(request)

    if student:
        future_events_q = [e.has_student(student) for e in future_events]
        future_rsvp_guests = [e.get_guests(student) for e in future_events]
        past_events_q     = [e.has_student(student) for e in past_events]
        past_rsvp_guests = [e.get_guests(student) for e in past_events]
    else:
        future_events_q = [False for e in future_events]
        future_rsvp_guests = [[] for e in future_events]
        past_events_q = [False for e in past_events]
        past_rsvp_guests = [[] for e in past_events]

        
    return render(request, 'events/events_list.html', {
      'error': '',
      'netid': permissions.get_username(request),
      'future_events': zip(future_events, future_events_q, future_rsvp_guests),
      'past_events' : zip(past_events, past_events_q, past_rsvp_guests),
    })  

@permissions.student
def events_signup(request, name, id):
    '''
        Based on the login, sign the person up for an event
    '''
    e = Event.objects.filter(id=id)
    s = permissions.get_student(request)

    # If we don't find the event then send them the error message
    if not e:  
        subject = 'The signup for this event %s is not available' % urllib.unquote(name)
        body = "Check back with us."
        return render(request, 'standard_message.html', {
                'subject' : subject,
                'body'    : body,
        })
    else:
        e = e[0]

    # Bounce Sophomores
    if not e.display_to_non_members and s.__class__.__name__ == 'Prospective':
        subject = 'Oops. %s' % urllib.unquote(name)
        body = "This event is not open for sophomores :/"

        return render(request, 'standard_message.html', {
                'subject' : subject,
                'body'    : body,
    })

    # If we find the event, then send them the form
    if request.method == 'POST':
        form = EventEntryForm(request.POST, event=e, student=s)

        if form.is_valid():
            form.execute_form_information()
    else:
        form = EventEntryForm(event=e,student=s)

    rsvp_entries = e.which_entries(s)
    rsvp_guests = e.get_guests(s)
    return render(request, 'events/events_signup.html', {
      'form' : form,
      'event' : e,
      'rsvp_entries': rsvp_entries,
      'rsvp_guests': rsvp_guests,

    })  

@permissions.officer
def events_officer_overview(request, name, id):
    '''
        Display all the data on this event
    '''
    event = Event.objects.filter(id=id)
    netid = permissions.get_username(request)
    officer = Officer.objects.filter(netid=netid)

    # If we don't find the event then send them the error message
    if not event:  
        subject = 'The signup for this event %s is not available' % urllib.unquote(name)
        body = "Check back with us."
        return render(request, 'standard_message.html', {
                'subject' : subject,
                'body'    : body,
        })
    else:
        event = event[0]

    return render(request, 'events/events_officer_overview.html', {
      'event' : event,
      'officer': officer,

    })  

@permissions.student
def entry_delete(request, name, entry_id):
    e = Entry.objects.filter(id=int(entry_id))
    s = permissions.get_student(request)

    # If we don't find the event then send them the error message
    if not e:  
        subject = 'The entry %s is not available' % urllib.unquote(name)
        body = "Check back with us."
        return render(request, 'standard_message.html', {
                'subject' : subject,
                'body'    : body,
        })
    else:
        e = e[0]

    # If we find the event, then send them the form
    if request.method == 'POST':
        form = EntryDeletionForm(request.POST, entry=e, student=s)

        if form.is_valid():
            form.delete_entry()
            return redirect('/' + e.event.get_signup_url())
    else:
        form = EntryDeletionForm(entry=e,student=s)

    return render(request, 'events/form.html', {
        'title': 'Event Deletion Form',
        'entry': e, 
        'form' : form,
        })


@permissions.student
def entry_change_answers(request, name, entry_id):
    e = Entry.objects.filter(id=int(entry_id))
    s = permissions.get_student(request)

    # If we don't find the event then send them the error message
    if not e:  
        subject = 'The entry %s is not available' % urllib.unquote(name)
        body = "Check back with us."
        return render(request, 'standard_message.html', {
                'subject' : subject,
                'body'    : body,
        })
    else:
        e = e[0]

    # If we find the event, then send them the form
    if request.method == 'POST':
        form = ChangeAnswersForm(request.POST, entry=e, student=s)

        if form.is_valid():
            form.change_answers()
            return redirect('/' + e.event.get_signup_url())
    else:
        form = ChangeAnswersForm(entry=e,student=s)

    return render(request, 'events/form.html', {
        'title': 'Entry Answer Change Form',
        'entry': e,
        'form' : form,
        })


@permissions.student
def entry_guest_change(request, name, entry_id):
    e = Entry.objects.filter(id=int(entry_id))
    s = permissions.get_student(request)

    # If we don't find the event then send them the error message
    if not e:  
        subject = 'The entry %s is not available' % urllib.unquote(name)
        body = "Check back with us."
        return render(request, 'standard_message.html', {
                'subject' : subject,
                'body'    : body,
        })
    else:
        e = e[0]

    # If we find the event, then send them the form
    if request.method == 'POST':
        form = ChangeGuestForm(request.POST, entry=e, student=s)

        if form.is_valid():
            form.change_guest()
            return redirect('/' + e.event.get_signup_url())
    else:
        form = ChangeGuestForm(entry=e,student=s)

    return render(request, 'events/form.html', {
        'title': 'Change Guest Form',
        'entry': e,
        'form' : form,
        })

@permissions.student
def entry_room_change(request, name, entry_id):
    e = Entry.objects.filter(id=int(entry_id))
    s = permissions.get_student(request)

    # If we don't find the event then send them the error message
    if not e:  
        subject = 'The entry %s is not available' % urllib.unquote(name)
        body = "Check back with us."
        return render(request, 'standard_message.html', {
                'subject' : subject,
                'body'    : body,
        })
    else:
        e = e[0]

    # If we find the event, then send them the form
    if request.method == 'POST':
        form = ChangeRoomForm(request.POST, entry=e, student=s)

        if form.is_valid():
            form.change_room()
            return redirect('/' + e.event.get_signup_url())
    else:
        form = ChangeRoomForm(entry=e,student=s)

    return render(request, 'events/form.html', {
        'title': 'Change Room Form',
        'description' : 'Because you must accompany your guest, changing rooms will move all of your guests with you.',
        'entry': e,
        'form' : form,
        })

# from events.models import Event, Room
# from events.forms import EventEntryForm, EventCreateForm, EventChoiceForm, EventEditForm

# ------------------------------------------------------------
# Responsible for creating entries to events. 
# 
# Chooses the event from the title and date parsed from the url. 
# ------------------------------------------------------------
# # @permissions.member
# def events_entry(request, title, date):
#   # Look for the event
#     start = parse_date(date)
#     end = start + datetime.timedelta(days=1)
#     event_search = Event.objects.filter(title=urllib.unquote(title), date_and_time__range = [start, end])


#     # If we don't find the event then send them the error message
#     if not event_search:  
#         subject = 'No Signups Available'
#         body = "Looks like there are no upcoming events with signups at the moment."
#         return render(request, 'standard_message.html', {
#                 'subject' : subject,
#                 'body'    : body,
#         })
#     event = event_search[0]
#     # If we do find it, give them the form
#     if request.method != 'POST':
#         form = EventEntryForm(event=event, netid=permissions.get_username(request))
#     # If the form is filled out, check it
#     else:
#         form = EventEntryForm(request.POST, event=event, netid=permissions.get_username(request))
#         if form.is_valid():
#             data =  form.cleaned_data
#             # Lookup the Member   
#             member = Member.objects.filter(netid=permissions.get_username(request))[0]
#             guest_s = "%s %s" % (form.cleaned_data['guest_first_name'], form.cleaned_data['guest_last_name'])
#             guest_s = guest_s.strip()

#             # Now try to add a person 
#             event.add_to_event(member, guest_s, form.cleaned_data['room_choice'])

#             return redirect('events')
#     return render(request, 'events/events_form.html', {
#         'form': form,
#         'event': event,
#         'error': '',
#         'netid': permissions.get_username(request),
#     })

# @permissions.member
# def events_view(request, title, date):
#     start = parse_date(date)
#     end = start + datetime.timedelta(days=1)
#     event_search = Event.objects.filter(title=urllib.unquote(title), date_and_time__range = [start, end])
    
#     # If we don't find the event then send them the error message
#     if not event_search:  
#         subject = "Doesn't look like this event exists"
#         body = "Checkout "
#         return render(request, 'standard_message.html', {
#                 'subject' : subject,
#                 'message' : body,
#         })

#     # If we find the event, show it to them
#     else:
#         event = event_search[0]

#         return render(request, 'events/events_view.html', {
#                      'error': '',
#                      'netid': permissions.get_username(request),
#                      'room_list' : event.to_JSON()['rooms'],
#         })  

#     # return HttpResponse("Hello, world. You're at a events view")
# @permissions.member
# def events_unrsvp(request, title, date):
#     start = parse_date(date)
#     end = start + datetime.timedelta(days=1)
#     event_search = Event.objects.filter(title=urllib.unquote(title), date_and_time__range = [start, end])
    
#     # If we don't find the event then send them the error message
#     if not event_search:  
#         subject = "Doesn't look like this event exists"
#         body = "Checkout "
#         return render(request, 'standard_message.html', {
#                 'subject' : subject,
#                 'message' : body,
#         })
#     else:
#         # Lookup the Member   
#         lookup_m =  Member.objects.filter(netid=permissions.get_username(request))
#         event = event_search[0]

#         if not lookup_m:
#             raise Exception('Error: Member with netid "%s" not found in member database' % request['netid']) 
#         member = lookup_m[0]

#         # If the member is in the room, take the person out. 
#         if event.has_member(member):
#             event.remove_from_event(member)
#             return redirect('events')
#         else:
#             return render(request, 'standard_message.html', {
#                 'subject' : 'No RSVP found',
#                 'message' : "are you sure you had RSVP'd to this event?",
#         })



# @permissions.officer
# def events_create(request):
#    #Generate Event Form
#    if request.method == 'POST':
#      form = EventCreateForm(request.POST)
#      if form.is_valid():
#         form.save()
#         return HttpResponseRedirect('thanks_create') # Redirect after POST
#    else:
#       form = EventCreateForm()

#    return render(request, 'events/events_create.html', {
#      'form': form,
#      'dropdown': EventEditForm(),
#      'error': '',
#      'netid': permissions.get_username(request),
#      # 'netid': permissions.get_username(request),
#    })  

 
# @permissions.officer
# def thanks_create(request):
#   return render(request, "events/thanks_create.html", {
#      'error': '',
#      'netid': permissions.get_username(request),
#   })

# @permissions.member
# def thanks_signup(request):
#   return render(request, "thanks_signup.html", {
#      'error': '',
#      'netid': permissions.get_username(request),
#   })
