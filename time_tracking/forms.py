# time_tracking/forms.py
from django.forms import ModelForm, CharField, DateField, DateInput, TimeField, TimeInput
from django.utils.translation import gettext_lazy as _
from .models import Time_Entry


class TimeTrackingForm(ModelForm):
    #datum = DateField(input_formats='%d.%m.%Y')
    date = DateField(widget=DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    #start = TimeField(input_formats='%H:%M')
    start = TimeField(widget=TimeInput(format = '%H:%M'), input_formats=('%H:%M',))
    end = TimeField(widget=TimeInput(format = '%H:%M'), input_formats=('%H:%M',))
    #project = CharField(max_length=10)
    class Meta:
        model = Time_Entry
        fields =  ['description', 'project_id']
        widgets = {
            'current_day': DateInput()
        }
        # labels = {
        #     'description': _('Beschreibung'),
        #     'project_id': _('Projekt'),
        #     'date': _('Datum'),
        #     'start_time': _('Start'),
        #     'end_time': _('Ende'),
        # }
        # help_texts = {
        #     'description': _('Was habe ich gemacht?'),
        # }
        error_messages = {
            'description': {
                'max_length': _('Die Beschreibung ist zu lang.'),
            },
        }

        # def __init__(self, *args, **kwargs):
        #     super(TimeTrackingForm, self).__init__(*args, **kwargs)
        #     self.fields['myfield'].widget.attrs.update({'class': 'myfieldclass'})