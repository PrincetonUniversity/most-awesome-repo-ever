from django import forms
from models import *

class GearItemForm(forms.Form):
    def __init__(self, fields, item, *args, **kwargs):
        super(GearItemForm, self).__init__(*args, **kwargs)
        #self.fields['name'] = forms.CharField(widget = forms.HiddenInput(), required = False, initial = item.name)
        sizes = []
        itemGroup = GearItem.objects.filter(name=item.name)
        for i in range(len(itemGroup)):
        	if ((itemGroup[i].sizes != '') and (itemGroup[i].inventory > 0)):
        		sizes.append(itemGroup[i].sizes)
        #sizes = item.sizes.split() #change to sizes, not name
        for i in range(len(sizes)):
        	sizes[i] = (sizes[i], sizes[i])
        if (len(sizes) > 0):
        	self.fields['size'] = forms.ChoiceField(sizes)
        else:
        	self.fields['size'] = forms.ChoiceField([("default", "default")])
        #if (item.custom_text > 0): #replace with if (item.custom_text > 0):
        	#self.fields[item.name+'_text'] = forms.CharField(max_length=10) #replace with custom_text
        quantity = []
        for i in range(1, 10):
        	quantity.append((i, i))
        self.fields['quantity'] = forms.ChoiceField(quantity)