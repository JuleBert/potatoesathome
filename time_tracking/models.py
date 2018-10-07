#time_tracking/models.py
from django.db import models
from django.utils import timezone
from django.utils.six import with_metaclass
from django.shortcuts import get_object_or_404
from _datetime import datetime

# python3 manage.py makemigrations time_tracking
# See the SQL:
# python3 manage.py sqlmigrate time_tracking 0001 
# python3 manage.py migrate


'''
class UpperCharField(with_metaclass(models.SubfieldBase, models.CharField)):
    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop('uppercase', False)
        super(UpperCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super(UpperCharField, self).get_prep_value(value)
        if self.is_uppercase:
            return value.upper()

        return value
'''
# Create your models here.
class Project(models.Model):
    project_code = models.CharField(max_length=10, unique=True)
    project_description = models.CharField(max_length=100, default = '')
    def __str__(self):
        return self.project_code + ' ' + self.project_description

class Overtime_Adjustment_Entry(models.Model):
    adjustment_date = models.DateField('adjustment_date')
    adjustment = models.DecimalField(max_digits=10, decimal_places=10)

class Time_Entry(models.Model):
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    description = models.CharField(max_length=250, default='')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=250) #models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    #def __str__(self):
        # my_project = get_object_or_404(Project, pk=self.project_id)
        #return str(self.get_day) + ' ' + self.project_id.project_code

    def format_timedelta(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return '{} h {} min'.format(hours, minutes)
        else:
            return str(minutes) + ' min'

    def get_duration(self):
        td = self.end_time - self.start_time
        return self.format_timedelta(td.seconds)

    def get_days_work(self):
        work_seconds = 0
        for today_entry in Time_Entry.objects.filter(start_time__date=self.start_time.date()):
            print(today_entry, today_entry.start_time, today_entry.end_time, today_entry.end_time - today_entry.start_time)
            days_work = today_entry.end_time - today_entry.start_time
            work_seconds += days_work.seconds
        return self.format_timedelta(work_seconds)

    def get_day(self):
        return str(self.start_time.date().strftime("%d.%m.%Y"))

    def get_day_if_first(self):
        return_value = ''
        if self.start_time == Time_Entry.objects.filter(start_time__date=self.start_time.date())[0].start_time:
            return_value = str(self.start_time.date().strftime("%d.%m.%Y"))
        return return_value

    def get_start(self):
        return str(self.start_time.strftime("%H:%M"))

    def get_end(self):
        return str(self.end_time.strftime("%H:%M"))
    
    def get_project_code(self):
        #my_project = get_object_or_404(Project, pk=self.project_id)
        return self.project_id.project_code
        
    def insert(self):
        self.created_at = timezone.now()
        self.save()
        
    def __str__(self):
        return self.get_day() + ' ' + self.project_id.project_code + ' ' + self.description
    