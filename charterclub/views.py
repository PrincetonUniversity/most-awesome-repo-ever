from django.http import HttpResponse, HttpResponseRedirect
from django import template
import django.shortcuts
from django.template import RequestContext
from django.template.loader import get_template
from django.conf import settings

import datetime
from datetime import date, timedelta

from forms import *
from events.models import *
# import configuration
from os import listdir, path
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone

import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response

from models import *
import permissions as permissions
from permissions import render

from ldap_student_lookup import get_student_info
from recruitment.forms import AccountCreationForm


from model_viewer import ProspectiveModelViewer
########################################################################
# Some easy one-age requests
# 
# Displays the membership of a target year
########################################################################
def index(request):
    return render(request, "index.html")


def history(request):
    return render(request, "flatpages_default/history.html")

def song(request):
    return render(request, "flatpages_default/song.html")

def constitution(request):
    return render(request, "flatpages_default/constitution.html")



def catering(request):
    manager = Staff.objects.all().order_by('order')

    if manager:
        manager = manager[0]
    else:
        manager = None

    return render(request, "flatpages_default/catering.html", {
          'manager' : manager,
      })

# allow user to view list of current officer corps.
def officer_list(request):

    olist = Officer.objects.all()

    query_s = Officer.objects.filter(is_active=True).order_by('order')
    top6 = query_s[:6]
    officer_rest = query_s[6:]

    return render(request, 'charterclub/officer_list.html', {
       'title' : 'Our Undergraduate Officers',
       'top6' : top6,
       'officer_rest' : officer_rest
    }) 

# allow user to view list of current officer corps.
def staff_list(request):
    olist = Staff.objects.all()

    query_s = Staff.objects.filter().order_by('order')
    top6 = query_s[:6]
    staff_rest = query_s[6:]

    return render(request, 'charterclub/staff_list.html', {
     'title' : 'Our Staff',
     'top6' : top6,
     'officer_rest' : staff_rest
    }) 

def contactus(request):
    now = datetime.datetime.now().date()

    prez = Officer.objects.filter(is_active=True).filter(position='President')
    vp = Officer.objects.filter(is_active=True).filter(position='Vice President')

    if not prez: 
      prez = ''
    else:
      prez = prez[0]


    if not vp:
      vp = ''
    else:
      vp = vp[0]


    return render(request, 'contactus.html', {
     'current_date': now,
     'netid': permissions.get_username(request),
     'prez': prez,
     'vp': vp,
    }) 


########################################################################
# Faceboard
# 
# Displays the current membership
########################################################################
def faceboard(request):
  
    # rollover = June 3nd
    senior_year = (date.today() - timedelta(days=153)).year + 1
    current_membership = Member.objects.filter(year__range=(senior_year, senior_year+2))
    year_options = Member.get_membership_years()

    return render(request, 'charterclub/faceboard.html', {
      'title':   'Current Membership',
      'year_options': reversed(year_options),
      'display_membership' : current_membership,
  })

########################################################################
# Faceboard_year
# 
# Displays the membership of a target year
########################################################################
def faceboard_year(request, year):
    # rollover = June 3nd
    members = Member.objects.filter(year=year)

    year_options = Member.get_membership_years()

    return render(request, 'charterclub/faceboard.html', {
      'title':   'Class of %s' % year,
      'year_options': reversed(year_options),
      'display_membership' : members,
    })


# Allows a member or a prospective to view their page
# DO NOT use the decorator permissions.member or permissions.prospective on this
#    The logic in this function will verify this information
def profile(request):
    # check their permissions
    netid_s = permissions.get_username(request)
    student = permissions.get_student(request)

    # Reject them if not valid netid
    if not netid_s:
        return render(request,"permission_denied.html",
                {"required_permission": "a Princeton student with a netid."}) 

    # For people not in our database
    if not student:
      if request.method == 'POST':
          form = AccountCreationForm(request.POST, netid=netid_s)
          if form.is_valid():
              prospective = form.create_account()
              
              return render(request, "recruitment/create_account_success.html", {
                      'prospective' : prospective,
                  })
      else:
          form = AccountCreationForm(netid=netid_s)

      return render(request,  "charterclub/login_no_account.html", {'form': form})


    
    future_entries = Entry.get_future_related_entries_for_student(student)
    past_entries = Entry.get_past_related_entries_for_student(student)

    # Show prospective page
    if student.__class__.__name__== 'Prospective':
        pmv = ProspectiveModelViewer(student.cast())

        return render(request, "charterclub/prospective_profile.html", {
              'prospective': student,
              'future_entries': future_entries,
              'prospective_model_viewer' : pmv,
              # 'events': e,
              'netid': permissions.get_username(request)
        })
              
    # Show members page 
    # if student.__class__.__name__ in ['Member', 'Officer']:
    return render(request, "charterclub/member_profile.html", {
        'member': student,
        'future_entries': future_entries,
        'netid': permissions.get_username(request)
    })



def permission_denied(request):
    return render(request, "permission_denied.html")

def underconstruction(request):
    return render(request, "underconstruction.html", {
    })

def error404(request):
    return render(request, "404.html")
