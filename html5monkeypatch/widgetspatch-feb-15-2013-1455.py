"""
This file is autoimported and patches at run time htmlt5 support for Django wigets
"""
from django.forms.widgets import Widget


# Patch the Django Widget class
widget_build_attrs_old = Widget.build_attrs 
def widget_build_attrs_patch(self, extra_attrs=None, **kwargs):
	""" 
	Adds folowing html5 attributes automatically:
		
		- required="required" attribute if field's 'is_required' is 'True'  	
	"""
	attrs = widget_build_attrs_old(self, extra_attrs=None, **kwargs)
	#if self.is_required == True:
	#	attrs["required"] = "required"

	
	#if hasattr(self, 'help_text'):
	#	attrs["placeholder"] = self.help_text
	return attrs
Widget.build_attrs =  widget_build_attrs_patch
del widget_build_attrs_patch # clean up namespace
#del widget_build_attrs_old # clean up namespace
