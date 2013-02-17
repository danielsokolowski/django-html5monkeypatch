"""
This file is autoimported and patches at run time htmlt5 support for Django
"""
from django.forms.fields import EmailField, URLField, Field, IntegerField, DecimalField
from html5monkeypatch.html5_wigets import EmailInput, URLInput, NumberInput

fields_widget_attrs_old = Field.widget_attrs 
def fields_widget_attrs_patch(self, widget):
	""" 
	Adds folowing html5 input attributes automatically by patching the .widget_attrs default Field hook method:
		- required="required" attribute if field's 'is_required' is 'True'
		- placeholder='<self.help_text>' - based on fields current 'help_text' value  	
	"""
	attrs = fields_widget_attrs_old(self, widget)
	if self.required == True:
		attrs["required"] = "required"
	if self.help_text is not "":
		attrs["placeholder"] = self.help_text
	if hasattr(self, 'min_value'):
		attrs["min"] = self.min_value
	if hasattr(self, 'max_value'):
		attrs["max"] = self.max_value
	if hasattr(self, 'decimal_places'):
		# covert decimal places to input step attribute if if decimal_places not specified default to step 0.1
		attrs['step'] = 1 * 10**(-1 * (self.decimal_places or 1))
	#FIXME: this does not work?! if hasattr(self, 'regex'):
		
		#attrs['pattern'] = self.regex 
		
	return attrs
Field.widget_attrs =  fields_widget_attrs_patch
del fields_widget_attrs_patch # clean up namespace

"""
Assign appropriate our new HTML5 widgets to existing django form fields
"""
EmailField.widget = EmailInput
URLField.widget = URLInput
IntegerField.widget = NumberInput
DecimalField.widget = NumberInput

