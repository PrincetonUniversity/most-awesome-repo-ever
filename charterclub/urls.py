from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import dajaxice
from dajaxice.core import dajaxice_config, dajaxice_autodiscover
from django.contrib.flatpages import views

dajaxice_autodiscover()
admin.autodiscover()
#Here is a mapping between the pattern in the URL to the function that
#   generates the page.
urlpatterns = patterns('',
    url(
        r'^$',
        'charterclub.views.index',
        name='index'), 
     url(
        r'^#$',
        'charterclub.views.index',
        name='index'), 
    url(
        r'^index$',
        'charterclub.views.index',
        name='index'),
    
    url(r'^events/',
        include('events.urls')),
    url(r'^recruitment/',
        include('recruitment.urls')),
    url(r'^menus/',
        include('menus.urls')),
    url(r'^feedback',
        include('feedback.urls')),
    url(
        r'^gear',
        'gear.views.gear',
        name='gear'),
    url(
        r'^cart',
        'gear.views.cart',
        name='cart'),


    url(r'^calendar', 
        include('django_bootstrap_calendar.urls')),

    url(r'^kitchen/',
        include('kitchen.urls')),

    url(
        r'^faceboard$',
        'charterclub.views.faceboard',
        name='faceboard'),
    url(
        r'^catering$',
        'charterclub.views.catering',
        name='catering'),
    url(
        r'^faceboard/([0-9]+)/$',
        'charterclub.views.faceboard_year',
        name='faceboard_year'),
    url(
        r'^profile$',
        'charterclub.views.profile',
        name='profile'),
    url(
        r'^history$',
        'charterclub.views.history',
        name='history'),
    url(
        r'^song$',
        'charterclub.views.song',
        name='song'),
    url(
        r'^constitution$',
        'charterclub.views.constitution',
        name='constitution'),
    url(
        r'^officer_list$',
        'charterclub.views.officer_list',
        name='officer_list'),
    url(
        r'^staff_list$',
        'charterclub.views.staff_list',
        name='staff_list'),
    url(
        r'^contactus$',
        'charterclub.views.contactus',
        name='contactus'),
    url(
        r'^underconstruction$',
        'charterclub.views.underconstruction',
        name='underconstruction'),
    # for CAS
    url(
        r'^accounts/login/$',
        'django_cas.views.login',
        name = 'login'),
    url(
        r'^accounts/logout/$',
        'django_cas.views.logout',
        name = 'logout'),
    
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    # Django Admin
    url(r'^admin/',include(admin.site.urls)),
    # Django Flatpages
    # url(r'^about/', include('django.contrib.flatpages.urls')),

    # For serving Media files
) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
+ [url(r'^(?P<url>.*/)$', views.flatpage),]

if settings.DEBUG == False:
    urlpatterns += patterns('', url(r'',
                                    'charterclub.views.error404',
                                    name='error404'))
    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

