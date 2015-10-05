from charterclub.permissions import render
import charterclub.permissions as permissions

from charterclub.models import Prospective
from charterclub.model_viewer import ProspectiveViewer

from kitchen.models import Meal, Brunch, Lunch, Dinner
from kitchen.forms import MealSignupForm

from django.utils import timezone
from django.utils.dateparse import parse_date
import datetime

# Displays the weekly menu for a specific day
def weekly_menu_day(request, date):
    # Find the relevant days
    target = parse_date(date)

    if not target:
        return render(request, 'standard_message.html', {
            'subject': 'Oops, looks like something went wonky.',
            'body' : 'Could note parse_date from "%s"' % (date)

            })

    prev_week = target + datetime.timedelta(weeks=-1)
    next_week = target + datetime.timedelta(weeks=1)

    monday = (target + datetime.timedelta(days=-target.weekday(), weeks=0))
    week = [monday + datetime.timedelta(days=i) for i in range(0,7)]
    
    meals_iter = []

    # Find the proper meals
    for day in week:
        brunch = Brunch.objects.filter(day=day) 
        lunch = Lunch.objects.filter(day=day)
        dinner = Dinner.objects.filter(day=day)

        # Dereference the hits
        if lunch:
            lunch = lunch[0]
        if dinner:
            dinner = dinner[0]
        if brunch:
            brunch = brunch[0]

        name = day.strftime("%a %m/%d")
        
        # Prevent both brunch and lunch from showing up, which screws up formatting
        if brunch:
            lunch = None        
        meals_iter.append((name, day, brunch, lunch, dinner))

    return render(request, 'kitchen/weekly_menu.html', {
        'meals_week' : meals_iter,
        'prev_week' : prev_week,
        'next_week' : next_week,
    })

def weekly_menu(request):
    return weekly_menu_day(request, timezone.now().date().isoformat())


# Uses a calender widget to sign up for meals
@permissions.prospective
def meal_signup(request):
    netid = permissions.get_username(request)
    prospective = Prospective.objects.filter(netid=netid)[0]
    pv = ProspectiveViewer(prospective)

    # Give them a form to fill out
    if request.method == 'POST':
        form = MealSignupForm(request.POST, prospective=prospective)
        if form.is_valid():
            form.add_prospective(prospective)
    else:
        form = MealSignupForm(prospective=prospective)

    # Look at the meals in the future
    future_meals =  Meal.objects.filter(day__gte=timezone.now())
    future_dates = sorted(set([m.day for m in future_meals]))
 
    # Figure out which ones are available
    available_dates = []
    calendar_date_to_text = {}

    for d in future_dates:
        m_a =  [m.cast() for m in Meal.objects.filter(day=d)]

        hover_text = []

        for m in m_a:
            hover_text.append("%s: %s" % ( m.__class__.__name__, m.sophomore_limit_text()))
            
            if m.num_of_sophomores() < m.sophomore_limit:
                available_dates.append(d)

        calendar_date_to_text[d.strftime("%Y-%m-%d")] = ",".join(hover_text)
        
    # Which days can the choose on the calender picker?
    dates_allowed = sorted(set([d.strftime("%Y-%m-%d") for d in available_dates]))

    #Get the meals that they ate this month
    now = timezone.now()
    prospective_this_month_meals = prospective.prospectivemealentry_set.filter(meal__day__gte=now)


    now = timezone.now()
    return render(request, 'kitchen/meal_signup.html', 
        {
            "prospective" : prospective,
            "prospective_viewer" : pv, 
            'form': form,
            'dates_allowed' : dates_allowed,
            'hover_text' : calendar_date_to_text,
            'now': now,
            'prospective_this_month_meals' : prospective_this_month_meals, 
        })

from django.core.exceptions import FieldError
from django.http import HttpResponse
from datetime import date
import json

def meal_info(request, month, day, year):
    '''
        Returns the information about a meal via a get request
    '''

    try:
        d = date(int(year), int(month), int(day))
    except:
        raise FieldError('Invalid Fields for /year/month/date in GET URL')
    
    brunch = Brunch.objects.filter(day=d) 
    lunch = Lunch.objects.filter(day=d)
    dinner = Dinner.objects.filter(day=d)

    data = {}
    string_s = ['brunch', 'lunch', 'dinner']
    meals_qa = [brunch, lunch, dinner]

    for string, meal_q in zip(string_s, meals_qa):
        if not meal_q:
            data[string] = (-1, -1)
        else:
            num_attending = len(meal_q[0].prospectivemealentry_set.all())
            num_limit = meal_q[0].sophomore_limit

            data[string] = (num_attending, num_limit)
    return HttpResponse(json.dumps(data), content_type="application/json")
