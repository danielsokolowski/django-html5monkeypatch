"""
This file is autoimported and patches at run time htmlt5 support for Django
"""
from django.forms.forms import BaseForm
from django.forms.widgets import Input, Textarea
from django.utils.html import conditional_escape, format_html
from django.utils.encoding import force_text
from django.utils import six
from django.utils.safestring import mark_safe
import inspect
import hashlib
import warnings


# Patch the Django Widget class
BaseForm._html_output_premonkeypatch = BaseForm._html_output
def baseform__html_output_patched(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
	"""
	Helper function for outputting HTML. Used by as_table(), as_ul(), as_p().
	 
	Our patched version strips help_text display as we by default now output it as a input 'placeholder' attribute.
	Based on current function code there is no easy way to string out the text from the output so we virtually have to 
	duplicate the code here and leave out the help_text string substition out.
	
	FYI: Setting help_text_html to '' results in a string substition error. 
	"""
	top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
	output, hidden_fields = [], []

	for name, field in self.fields.items():
		html_class_attr = ''
		bf = self[name]
		bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
		if bf.is_hidden:
			if bf_errors:
				top_errors.extend(['(Hidden field %s) %s' % (name, force_text(e)) for e in bf_errors])
			hidden_fields.append(six.text_type(bf))
		else:
			# Create a 'class="..."' atribute if the row should have any
			# CSS classes applied.
			css_classes = bf.css_classes()
			if css_classes:
				html_class_attr = ' class="%s"' % css_classes

			if errors_on_separate_row and bf_errors:
				output.append(error_row % force_text(bf_errors))

			if bf.label:
				label = conditional_escape(force_text(bf.label))
				# Only add the suffix if the label does not end in
				# punctuation.
				if self.label_suffix:
					if label[-1] not in ':?.!':
						label = format_html('{0}{1}', label, self.label_suffix)
				label = bf.label_tag(label) or ''
			else:
				label = ''
				
			# we try to follow per http://www.wufoo.com/html5/attributes/01-placeholder.html specs and disable
			# help text for some elements as in our patch_widgets we make help_text = placeholder
			if field.help_text and not isinstance(field.widget, Input) and not isinstance(field.widget, Textarea):
				help_text = help_text_html % force_text(field.help_text)
			else:
				# some certain Input types should still have help_text rather than not
				if hasattr(field.widget, 'input_type') and field.widget.input_type in ['file']:
					help_text = help_text_html % force_text(field.help_text)
				else:
					help_text = ''
			
			output.append(normal_row % {
				'errors': force_text(bf_errors),
				'label': force_text(label),
				'field': six.text_type(bf),
				'help_text': help_text,
				'html_class_attr': html_class_attr
			})

	if top_errors:
		output.insert(0, error_row % force_text(top_errors))

	if hidden_fields: # Insert any hidden fields in the last row.
		str_hidden = ''.join(hidden_fields)
		if output:
			last_row = output[-1]
			# Chop off the trailing row_ender (e.g. '</td></tr>') and
			# insert the hidden fields.
			if not last_row.endswith(row_ender):
				# This can happen in the as_p() case (and possibly others
				# that users write): if there are only top errors, we may
				# not be able to conscript the last row for our purposes,
				# so insert a new, empty row.
				last_row = (normal_row % {'errors': '', 'label': '',
										  'field': '', 'help_text':'',
										  'html_class_attr': html_class_attr})
				output.append(last_row)
			output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
		else:
			# If there aren't any rows in the output, just append the
			# hidden fields.
			output.append(str_hidden)
	return mark_safe('\n'.join(output)) 	

BaseForm._html_output  =  baseform__html_output_patched # monkey patch our version in
del baseform__html_output_patched # clean up namespace

# Because of how we are patching above let's at least throw a warning if old method signature changed from what we expect
if not '5eb59ca5b7ce7cb472ea43427cb7f819' == \
		hashlib.md5(inspect.getsource(BaseForm._html_output_premonkeypatch)).hexdigest():
	warnings.warn('md5 signature of BaseForm._html_output does match because Django code has been updated. There is a '
				  'slight change patch might be broken so please compare and update the monkeypatched method.')
	