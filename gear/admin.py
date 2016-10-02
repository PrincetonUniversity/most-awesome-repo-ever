from django.contrib import admin
from gear.models import GearItem

class GearItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'price', 'image_url')
	list_editable = ('name', 'description', 'price', 'image_url')
	ordering = ['name', 'description']

admin.site.register(GearItem, GearItemAdmin)