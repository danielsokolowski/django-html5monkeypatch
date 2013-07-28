###HTML5 monkey patched support for django.

Monkeys are *not* evil! Think of monkeypatching as a way to do advanced settings for your Django project. Based on that
assumption this App is an experiment and proof of concept. It provides HTML5 django support by default and without 
having to update your existing code, for example you might have did this in the past:

	Before:
	
		class HTML5DateTimeInput(django.forms.widgets.DateTimeInput):
		    """Subclass TextInput since there's no direct way to override its 'type' attribute"""
		    if settings.USE_TZ:
				input_type = 'datetime'
			else:
				input_type = 'datetime-local'
		
		class MyModelForm(ModelForm):
		    class Meta:
		        model = MyModel
		        widgets = {
		            'thedatetimefield': HTML5DateTimeInput(attrs={'required':'required'})
		            # our Model's DateTimeField is set 'blank=False'
		        }
	
	After:
	
		class MyModelForm(ModelForm):
		    class Meta:
		        model = MyModel

That's right: by including this app in your settings all your current DateTimeFields (native or aware) on your Forms or 
Model forms will render now as html5 &lt;input type="datetime" ...&gt;' or '&lt;inpyt type="datetime-local" ... &gt;' widgets. 

##Features

1. automatic django built in form field mapping to corresponding HTML5 input types (widgets):
	* 'django.forms.fields.EmailField' maps to '&lt;input type="email" ...&gt;'
	* 'django.forms.fields.URLField' maps to '&lt;input type="url" ...&gt;'
	* 'django.forms.fields.IntegerField' maps to '&lt;input type="number" min="&lt;field.min_value&gt;" max="&lt;field.max_value&gt;" ...&gt;
	* 'django.forms.fields.DecimalField' maps to '&lt;input type="number" min="&lt;field.min_value&gt;" max="&lt;field.max_value&gt;"
	   step="&lt;field.decimal_places converted to step value or 0.1 if None&gt;
2. HTML5 form, model form, and widget input support for:
	* color, date, datetime, datetime-local, email, month, number, range, search, tel, time, url, week
3. HTML5 *automatic mapping* attribute support for followinng:
	- New attributes for &lt;form&gt;:
		* TODO: autocomplete
		* TODO: novalidate
	- New attributes for &lt;input&gt;:
		* placeholder
		* required  - maps from all form fields from Field.required
		* step - maps from DecimalField.decimal_places
		* min and max - maps from field has .min_value, or .max_value
		* TODO: autocomplete,  
		* TODO: autofocus
		* TODO: form
		* TODO: formaction
		* TODO: formenctype
		* TODO: formmethod
		* TODO: formnovalidate
		* TODO: formtarget
		* TODO: height and width
		* TODO: list
		* TODO: multiple
		* TODO: pattern (regexp)
4. no JS fallback pollution - let the browser support handle it or you may sprinkle JS yourself (might change this)
5. help_text is no longer rendered outside of input tag (patched BaseForm._html_output)
6. help_text is mapped onto placeholder input attribute: '&lt;input type="text" placeholder="&lt;help_text" ...&gt;' but 
   only for elements that it make sense to do so otherwise help_text is rendered with the field as in original.  

## Installation

You are encouraged to hack this into your project rather then use it as a stand alone app - in my experience
it's cleaner to hack code directly rather then sublcass. 

	git clone --origin danielsokolowski git://github.com/danielsokolowski/django-html5monkeypatch.git

Include this application somewhat at the top of your settings.py files, so that the patch is applied early during 
Django start initialization:

	INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.flatpages',
	'django.contrib.admin',
	'django.contrib.gis',

	# Stand alone APPS - see any app specific settings at bottom of this settings.py file
	'html5monkeypatch', 
	)
	
## Well behaved Monkeypatch Example

IMHO below is an example of a well behaved patch, verbose and obvious is good, this evolved over a few iterations and 
your comments are welcomed on this approach:

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
	    MONKEYPATCHED: Adds new html5 input attributes support by automatically mapping from the Field instance:
	    """
	    ...
	    < do patchy things > ...
	    ...    
	    return attrs
	widget_attrs_monkeypatched.__doc__ += Field.widget_attrs.__doc__  # be still super nice and update the docstring
	
	# do the actual patch
	Field.widget_attrs = widget_attrs_monkeypatched
	del widget_attrs_monkeypatched  # clean up namespace

## Credits

Inspired by github: rhec / django-html5 but completely different. 