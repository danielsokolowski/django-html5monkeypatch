"""
This file is auto imported and patches any django widgets for  htmlt5 support
"""
from django.forms.widgets import DateInput , DateTimeInput, TimeInput
from django.conf import settings

DateInput.input_type = 'date'
# If our project uses 'aware' timezones then we ought to use tiemzone enabled HTML5 input time or local otherwise
if settings.USE_TZ:
	DateTimeInput.input_type = 'datetime'
else:
	DateTimeInput.input_type = 'datetime-local'

TimeInput.input_type = 'time'