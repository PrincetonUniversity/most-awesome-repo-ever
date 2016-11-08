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
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages

def cart(request):
    cart = Cart(request.session)

    if (request.method == 'GET'):
        if ("clear" in request.GET):
            cart.clear()
            return HttpResponseRedirect("/cart")
        for item in cart.items:
            if ("add" + item.product.name + item.product.sizes in request.GET):
                product = GearItem.objects.filter(name=item.product.name,
                    sizes=item.product.sizes)[0]
                if (int(item.quantity) < int(product.inventory)):
                    print "enough"
                    cart.add(product, product.price, 1)
                    message = "1 " + product.name + " (" + product.sizes + ") added to cart"
                    messages.success(request, message)
                else:
                    print "not enough"
                    message = "The amount of " + product.name + \
                    " requested is more than the amount we currently have - unable to add to cart"
                    messages.error(request, message)
                return HttpResponseRedirect("/cart")
            if ("sub" + item.product.name + item.product.sizes in request.GET):
                product = GearItem.objects.filter(name=item.product.name,
                    sizes=item.product.sizes)[0]
                quant = item.quantity - 1
                cart.remove(product)
                if (quant > 0):
                    cart.add(product, product.price, quant)
                message = "1 " + product.name + " (" + product.sizes + ") removed from cart"
                messages.success(request, message)
                return HttpResponseRedirect("/cart")




    for item in cart.items:
        print item.product.name
        print item.product.sizes
        print item.quantity
        print item.subtotal

    
    items = ""
    for item in cart.items:
        items = items + item.product.name + "|" + str(item.quantity) + "|" + item.product.sizes + "|"


    host = request.get_host()

    #pass variables to paypal
    paypal_dict = {"business": "receiver_email@example.com", 
        "invoice": "unique-invoice-id",
        "notify_url": host + "/paypal",
        "return_url": host + "/confirm",
        "cancel_return": host + "/cart",
        "shopping_url" : host + "/gear",
        "amount": cart.total,
        "item_name": "Gear Order",
        "custom": items,
        "on0": "test",
        "os0": items}

    print paypal_dict
    # What you want the button to do.

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, 'gear/cart.html', context)

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
                if (gear_list[i].sizes != ""):
                    product = GearItem.objects.filter(name=gear_list[i].name,
                    sizes=request.POST[('size')])[0]
                else: 
                    product = GearItem.objects.filter(name=gear_list[i].name)[0]
                print product
                quantity = request.POST[('quantity')]
                print quantity
                print product.inventory
                newQuantity = int(quantity)
                for item in cart.items:
                    if item.product == product:
                        newQuantity = newQuantity + int(item.quantity)
                if (newQuantity <= int(product.inventory)):
                    print "enough"
                    cart.add(product, product.price, quantity)
                    message = quantity + " " + product.name + " (" + product.sizes + ") added to cart"
                    messages.success(request, message)
                else:
                    print "not enough"
                    message = "The amount of " + product.name + \
                    " requested is more than the amount we currently have - unable to add to cart"
                    messages.error(request, message)
                print "added to cart"
                print cart.items
                print cart
                print cart.total
                return HttpResponseRedirect("/gear")
                break


    added = []
    for i in range(len(gear_list)):
        if ((gear_list[i].name not in added) and (gear_list[i].inventory > 0)):
            print added

            temp = {}
            temp['item'] = gear_list[i]
            temp['form'] = GearItemForm({}, gear_list[i])
            gear.append(temp)
            added.append(gear_list[i].name)

    gear_rows = []
    for i in range(int((len(gear) - 1)/ 3) + 1):
        i = (3*i)
        temp = {}
        if (i < len(gear)):
            temp['first'] = gear[i]
        if (i + 1 < len(gear)):
            temp['second'] = gear[i+1]
        if (i + 2 < len(gear)):
            temp['third'] = gear[i+2]
        if (temp['first']):
            gear_rows.append(temp)


    return render(request, 'gear/gear_flex.html', {
        'gear_list' : gear
        })

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

def testBuy(request):
    cart = Cart(request.session)
    items = cart.items
    for i in range(len(items) / 3):
            name = 3 * i
            quantity = 3 * i + 1
            size = 3 * i + 2
            product = GearItem.objects.filter(name=name,
                    sizes=size)[0]
            product.inventory = product.inventory - quantity
            product.save()

from decimal import *

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != "receiver_email@example.com":
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.

        items = ipn_obj.custom.split('|')
        price = 0

        for i in range(len(items) / 3):
            name = 3 * i
            quantity = 3 * i + 1
            size = 3 * i + 2
            product = GearItem.objects.filter(name=name,
                    sizes=size)[0]
            price = price + (product.price * quantity)
        
        #check that the money received is correct
        if Decimal(price) != ipn_obj.amount:
            return
        
        #update inventory
        for i in range(len(items) / 3):
            name = 3 * i
            quantity = 3 * i + 1
            size = 3 * i + 2
            product = GearItem.objects.filter(name=name,
                    sizes=size)[0]
            product.inventory = product.inventory - quantity
            product.save()

def confirm(request):
    return render(request, "gear/confirm.html")


valid_ipn_received.connect(show_me_the_money)