""" This file is autoimported and patches in at run time htmlt5 support for Django """
from django.forms.fields import EmailField, URLField, Field, IntegerField, DecimalField, SplitDateTimeField, TimeField
from html5monkeypatch.html5_wigets import EmailInput, URLInput, NumberInput
from django.forms.widgets import DateInput , DateTimeInput, TimeInput
import hashlib
import logging
import inspect
logger = logging.getLogger(__name__)

# be nice and tell you are patching
logger.info("Patching 'Field.widget_attrs = widget_attrs_monkeypatched': Adds new html5 input attributes support by "
			" automatically mapping from the Field instance")

# be nicer and confirm signature of code we are patching and warn if it has changed
# raise Exception(hashlib.md5(inspect.getsource(Field.widget_attrs)).hexdigest()) # uncommet to find latest hash
if not 'fdd8b32e3c5d782f7af69b29bf1b933b' == \
		hashlib.md5(inspect.getsource(Field.widget_attrs)).hexdigest():
	logger.warn("md5 signature of 'Field.widget_attrs' does not match Django 1.5. There is a slight chance patch "
					"might be broken so please compare and update this monkeypatch.")

Field.widget_attrs_premonkeypatch = Field.widget_attrs 
def widget_attrs_monkeypatched(self, widget):
	"""
	MONKEYPATCHED: Adds new html5 input attributes support by automatically mapping  from the Field instance:

		- required="required" attribute if field's 'is_required' is 'True'
		- placeholder='<self.help_text>' - based on fields current 'help_text' value
		- min='<self.min_value'> - based onf fields 'min_value'
		- max='<self.max_value'> - based onf fields 'max_value'
		- step=<decimal places converted> - if decimal_places is not specified defaeults to step 0.1

	"""
	attrs = self.widget_attrs_premonkeypatch(widget)
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
		attrs['step'] = 1 * 10 ** (-1 * (self.decimal_places or 1))
	if isinstance(self, SplitDateTimeField) or isinstance(self, TimeField):
		attrs['step'] = 1
	# FIXME: this does not work?! if hasattr(self, 'regex'):
		
		# attrs['pattern'] = self.regex 
		
	return attrs
widget_attrs_monkeypatched.__doc__ += Field.widget_attrs.__doc__  # be still super nice and update the docstring

# do the actual patch
Field.widget_attrs = widget_attrs_monkeypatched
del widget_attrs_monkeypatched  # clean up namespace

"""
Assign appropriate new HTML5 widgets to existing django form fields

TODO: add monkeypatching verbosity as above
"""
EmailField.widget = EmailInput
URLField.widget = URLInput
IntegerField.widget = NumberInput
DecimalField.widget = NumberInput

