from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(
        r'^weekly_menu$', 
        'kitchen.views.weekly_menu', 
        name='weekly_menu'),
        url(
    r'^weekly_menu/([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})$', 
        'kitchen.views.weekly_menu_day', 
        name='weekly_menu_day'),
    url(
        r'^meal_signup$', 
        'kitchen.views.meal_signup', 
        name='meal_signup'),
    url(
        r'^meal_info/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})$', 
        'kitchen.views.meal_info', 
        name='meal_info'),
    url(
        r'^meal_cancellation/(\d+)/(\d+)/(\w+)/(.+)', 
        'kitchen.views.meal_cancellation', 
        name='meal_cancellation'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
