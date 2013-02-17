from django.forms.widgets import Input

class EmailInput(Input):
	"Email HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'email'
	
class URLInput(Input):
	"URL HTML5 input type - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'url'

class NumberInput(Input):
	"Number HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'number'

### The inputs below don't have equivalent mapping django form fields	
class SearchInput(Input):
	"Search HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'search'
	
class ColorInput(Input):
	"Search HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'color'

class WeekInput(Input):
	"Week HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'week'
	
class MonthInput(Input):
	"Month HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'month'

class TelephoneInput(Input):
	"Telephone HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'tel'
	
class RangeInput(Input):
	"Range HTML5 input widget - unsupported browsers should gracefully degrade to input type='text' ...>"
	input_type = 'range'