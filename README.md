###HTML5 monkey patched support for django.

Monkeys are *not* evil! Think of monkeypatching as advanced default settings for your Django project. Based on that
assumption this App should be considered an experiment and proof of concept; it provides HTML5 django
support by default and without having to update your existing code.

	Before:
	
		class HTML5DateTimeInput(django.forms.widgets.DateTimeInput):
		    """Subclass TextInput since there's no direct way to override its type attribute"""
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
	
		# No subclassing of ModelForm needed
		
That's right: by including this app in your settings all your current DateTimeFields (native or aware) on your Forms or 
Model forms will render now as html5 &lt;input type="datetime" ...&gt;' or '&lt;inpyt type="datetime-local" ... &gt;' widgets. 

##Features

- automatic django built in form field mapping to corresponding HTML5 input types (widgets)
	* 'django.forms.fields.EmailField' maps to '&lt;input type="email" ...&gt;'
	* 'django.forms.fields.URLField' maps to '&lt;input type="url" ...&gt;'
	* 'django.forms.fields.IntegerField' maps to '&lt;input type="number" min="&lt;field.min_value&gt;" max="&lt;field.max_value&gt;" ...&gt;
	* 'django.forms.fields.DecimalField' maps to '&lt;input type="number" min="&lt;field.min_value&gt;" max="&lt;field.max_value&gt;"
	   step="&lt;field.decimal_places converted to step value or 0.1 if None&gt;
- HTML5 form, model form, and widget input support for:
	* color
	* date
	* datetime
	* datetime-local
	* email
	* month
	* number
	* range
	* search
	* tel
	* time
	* url
	* week
- HTML5 *automatic mapping* attribute support for followinng:
	- New attributes for &lt;form&gt;:
		TODO: autocomplete
		TODO: novalidate
		
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
		vTODO: pattern (regexp)
				
- no JS fallback pollution - let the browser support handle it or you may sprinkle JS yourself (might change this)
- help_text is no longer rendered outside of input tag (patched BaseForm._html_output)
- help_text is mapped onto placeholder input attribute: '&lt;input type="text" placeholder="&lt;help_text" ...&gt;'

## Installation

You are encouraged to hack this into your project rather then use it as a stand alone app - in my experience
projects end up saner that way. 

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

	# Stand alone APPS - see any specific settings at bottom of settings.py file
	'html5monkeypatch', 
	)
	
##Credits

Inspired by github: rhec  / django-html5 but completely different. 