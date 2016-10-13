from django import forms
from models import *

class GearItemForm(forms.Form):
    def __init__(self, fields, item, *args, **kwargs):
        super(GearItemForm, self).__init__(*args, **kwargs)
        #self.fields['name'] = forms.CharField(widget = forms.HiddenInput(), required = False, initial = item.name)
        sizes = item.sizes.split() #change to sizes, not name
        for i in range(len(sizes)):
        	sizes[i] = (sizes[i], sizes[i])
        if (len(sizes) > 0):
        	self.fields[item.name+'_sizes'] = forms.ChoiceField(sizes)
        if (item.custom_text > 0): #replace with if (item.custom_text > 0):
        	self.fields[item.name+'_text'] = forms.CharField(max_length=10) #replace with custom_text
        quantity = []
        for i in range(10):
        	quantity.append((i, i))
        self.fields[item.name+'_quantity'] = forms.ChoiceField(quantity)