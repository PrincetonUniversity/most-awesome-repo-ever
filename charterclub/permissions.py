import urllib2, json

import django.shortcuts
from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import User

import models
from models import Officer
from models import Member
from models import Student

from charterclub.models import Prospective, Member, Officer

#TODO do we use most of this right no? or only a piece?

# the following are decorator functions that indicate permissions required
# to view a page.

# e.g., in any views.py, the following indicates that myview
# can only be accessed by members

# import charterclub.permissions
# ...
# ...
# @permissions.member
# def myview(request):
#     render(request, "myview.html")

#######################################################
# These are decorator functions
#
#######################################################
def privileged(func):
	def check_p(request, *args, **kwargs):
		if not check_staff(request):
			return render(request, "permission_denied.html",
						  {"required_permission": "privileged"})
		return func(request, *args, **kwargs)
	return check_p

def officer(func):
    def check_o(request, *args, **kwargs):
        if not check_officer(request):
            return render(request, "permission_denied.html",
                          {"required_permission": "officer"})
        return func(request, *args, **kwargs)
    return check_o

def student(func):
    def check_o(request, *args, **kwargs):
        if not check_student(request):
            return render(request, "permission_denied.html",
                          {"required_permission": "student"})
        return func(request, *args, **kwargs)
    return check_o


def member(func):
    def check_m(request, *args, **kwargs):
        if not check_member(request):
            return render(request, "permission_denied.html",
                          {"required_permission": "member"})
        return func(request, *args, **kwargs)
    return check_m

def prospective(func):
    def check_s(request, *args, **kwargs):
        if not check_prospective(request):
            return render(request, "permission_denied.html",
                          {"required_permission": "prospective"})
        return func(request, *args, **kwargs)
    return check_s


def additional_context(request):
    '''
        Does a search of the database and returns the results
    '''
    def dereference(query_a):
        "Unwraps a query set"
        if len(query_a):
          return query_a[0]
        else:
          return None 

    netid = get_username(request)
    
    # Lookup people
    priv = None
    if (check_your_privilege(request)):
        priv = netid
    o = dereference(Officer.objects.filter(netid=netid))
    m = dereference(Member.objects.filter(netid=netid))
    p = dereference(Prospective.objects.filter(netid=netid))
    now = timezone.now()

    # Then return the results with the proper object pointers
	# TODO see if we can merge down these cases (eg do we need the o case or do we get member already?)
    if o:
        return { "netid": netid, "privileged": priv, "officer" : o, "member" : o.member, "student" : o.member.student, "prospective" : p, 'now': now}
    if m:  
        return { "netid": netid, "privileged": priv, "officer" : o, "member" : m, "student" : m.student, "prospective" : p, 'now': now}
    if p:
        return { "netid" : netid, "privileged": priv, "officer" : o, "member" : m, "student" : p.student, "prospective" : p, 'now': now}

    return  { "netid": netid, "privileged": priv, "officer" : None, "member" : None, "student" : None, "prospective" : None}


# a replacement render function which passes some additional
# user information to our template by wrapping the original
# render function. specifically, it passes information about the
# student/member/officer status of the user.
def render(request, template_name, context=None, *args, **kwargs):
    add_context = additional_context(request)
    if context:
        add_context.update(context)

    return django.shortcuts.render(request, template_name, add_context,
                                   *args, **kwargs)




# get the username of the currently CAS logged-in user.
# if there is no currently logged-in user, return an empty string
# if the application is in debug mode, assume that CAS is non-functional,
# and return a test value (in this case jwhitton)
def get_username(request):
    if settings.CAS_DISABLED:
        return "testuser"
    else:
        if not request.user.username:
            return ""
        else:
            return request.user.username


def get_student(request):
    '''
        Checks the login and takes the highest priority one.
    '''

    query = additional_context(request)
	
    if query['officer']:
        return query['officer']
    if query['member']:
        return query['member']
    if query['prospective']:
        return query['prospective']
    if query['student']:
        return query['student']

    return None

def tigerbooks_lookup(netid):
    '''
        Make a get request to tigerbooks API to find information.
    '''

    base_url = 'https://tigerbook.herokuapp.com/api/APnwzuMmFu2UTWVMtil7/'
    url = base_url + netid

    try:
        response = urllib2.urlopen(url)
        html_s = response.read()
        return json.loads(html_s)
    except:
        return None

# check if the currently CAS logged-in user is staff, returning
# true if so and false otherwise.
def check_your_privilege(request):
    usr = get_username(request)
    if usr == "":
        return False

    user = User.objects.filter(username=usr)

    if len(user) == 0:
        return False
    elif (user[0].is_staff):
        return True
	return False
 


# check if the currently CAS logged-in user is an officer, returning
# true if so and false otherwise.
def check_officer(request):
    netid = get_username(request)
    if netid == "":
        return False

    user = Officer.objects.filter(netid=netid)

    if len(user) == 0:
        return False
    else:
        return True
    
# check if the currently CAS logged-in user is a member, returning
# true if so and false otherwise.
def check_member(request):
    netid = get_username(request)
    if netid == "":
        return False

    user = Member.objects.filter(netid=netid)

    if len(user) == 0:
        return False
    else:
        return True

# check if the currently CAS logged-in user is a prospective, returning
# true if so and false otherwise.
def check_prospective(request):
    netid = get_username(request)
    if netid == "":
        return False

    user = Prospective.objects.filter(netid=netid)

    if len(user) == 0:
		return False
    else:
        return True

# check if the currently CAS logged-in user is a member, returning
# true if so and false otherwise.
def check_student(request):
    netid = get_username(request)
    if netid == "":
        return False

    user = Student.objects.filter(netid=netid)

    if len(user) == 0:
        return False
    else:
        return True

# import datetime
# import ldap_student_lookup

##### - The following code might be broken, so we're going to leave it out ####
# check if the currently CAS logged-in user is a sophomore, returning
# true if so and false otherwise. probably currently nonfunctional
# due to princeton-ldap not working on heroku
# def check_sophomore(request):
#     netid = get_username(request)
#     if netid == "":
#         return False

#     if len(ldap_student_lookup.ldap_lookup("netid=" + netid)) == 0:
#         return False
    
#     student = ldap_student_lookup.get_student_info(netid)

#     # check that the student's graduation year indicates they are currently
#     # a sophomore. e.g. a student graduating in 2017 is a sophomore if we are
#     # currently in the latter half of 2014 or the beginning half of 2015.
#     today = datetime.date.today()
#     year = (today + datetime.timedelta(days = 6*30))
#     if student.year == (year + 2):
#         return True
#     return False


