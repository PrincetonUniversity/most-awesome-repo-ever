from django.http import HttpResponse, HttpResponseRedirect
from django import template
import django.shortcuts
from django.template import RequestContext
from django.template.loader import get_template
from django.conf import settings

from forms import *

import datetime
from datetime import date, timedelta

from events.models import *
# import configuration
from os import listdir, path
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone

import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response

from models import *
from charterclub.permissions import render
from carton.cart import Cart
import logging
import chromelogger as console

def cart(request):
    return render(request, 'gear/cart.html')

def gear(request):

    print "\n"
    print "test 123 test"
    print "\n"
    print request.method

    gear_list = GearItem.objects.all()
    gear = []

    if (request.method == 'POST'):
        print "\n"
        print "hello"
        print "\n"
        print request.POST
        for i in range(len(gear_list)):
            print "btn_" + gear_list[i].name
            if (("btn_" + gear_list[i].name) in request.POST):
                print "\n"
                print "found a form"
                print "\n"
                cart = Cart(request.session)
                product = {}
                product['name'] = gear_list[i].name
                if ('sizes' in request.POST):
                    product['size'] = request.POST["sizes"]
                else:
                    product['size'] = ""
                if ('custom text' in request.POST):
                    product['text'] = request.POST["custom text"]
                else:
                    product['text'] = ""
                cart.add(gear_list[i], gear_list[i].price, 1)
                print "added to cart"
                print cart.items
                print cart
                print cart.total


    for i in range(len(gear_list)):
        temp = {}
        temp['item'] = gear_list[i]
        temp['form'] = GearItemForm({}, gear_list[i])
        gear.append(temp)
    return render(request, 'gear/gear.html', {
        'gear_list' : gear
        })