# time_tracking/forms.py
from django.forms import ModelForm, CharField, DateField, DateInput, TimeField, TimeInput, DecimalField
from django.utils.translation import gettext_lazy as _
from .models import Time_Entry, Project, SettingsModel, Overtime_Entry


class TimeTrackingForm(ModelForm):
    date = DateField(widget=DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    start = TimeField(widget=TimeInput(format = '%H:%M'), input_formats=('%H:%M',))
    end = TimeField(widget=TimeInput(format = '%H:%M'), input_formats=('%H:%M',))
    class Meta:
        model = Time_Entry
        fields =  ['description', 'project_id']
        widgets = {
            'current_day': DateInput()
        }
        error_messages = {
            'description': {
                'max_length': _('Die Beschreibung ist zu lang.'),
            },
        }



class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        #fields = ('project_code', 'project_description', 'employer')
        exclude = ('user_id',)

class SettingsForm(ModelForm):
    start_date = DateField(widget=DateInput(format='%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    class Meta:
        model = SettingsModel
        #fields = ('work_time_mon', 'work_time_tur', 'work_time_wed', 'work_time_thu', 'work_time_fri', 'work_time_sat', 'work_time_sun', 'start_date',)
        exclude = ('created_at', 'user_id',)

class OvertimeForm(ModelForm):
    class Meta:
        model = Overtime_Entry
        #fields = ('work_time_mon', 'work_time_tur', 'work_time_wed', 'work_time_thu', 'work_time_fri', 'work_time_sat', 'work_time_sun', 'start_date',)
        exclude = ('user_id',)