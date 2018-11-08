#time_tracking/models.py
from django.db import models
from django.utils import timezone
from django.utils.six import with_metaclass
from django.shortcuts import get_object_or_404
from _datetime import datetime
from django.contrib.auth.models import User as DjangoUser

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
    user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default='1')
    project_code = models.CharField('Projektcode', max_length=10, unique=True)
    project_description = models.CharField('Projektbeschreibung', max_length=100, default = '')
    emp_options = (
        ('AVGL', 'Avantgarde-labs'),
        ('CE', 'Conrad'),
    )
    employer = models.CharField('Arbeitgeber', max_length=20, choices=emp_options, default = 'AVGL')
    def __str__(self):
        return str(self.project_code) + ' ' + str(self.project_description)

class SettingsModel(models.Model):
    user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default='1')
    created_at = models.DateTimeField(default=timezone.now)
    start_date = models.DateField('Startdatum')
    work_time_mon = models.DecimalField('Arbeitszeit Montag', max_digits=10, decimal_places=2)
    work_time_tur = models.DecimalField('Arbeitszeit Dienstag', max_digits=10, decimal_places=2)
    work_time_wed = models.DecimalField('Arbeitszeit Mittwoch', max_digits=10, decimal_places=2)
    work_time_thu = models.DecimalField('Arbeitszeit Donnerstag', max_digits=10, decimal_places=2)
    work_time_fri = models.DecimalField('Arbeitszeit Freitag', max_digits=10, decimal_places=2)
    work_time_sat = models.DecimalField('Arbeitszeit Samstag', max_digits=10, decimal_places=2)
    work_time_sun = models.DecimalField('Arbeitszeit Sonntag', max_digits=10, decimal_places=2)


class Overtime_Entry(models.Model):
    user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default='1')
    overtime_date = models.DateField('Datum')
    overtime = models.DecimalField('Überstunden', max_digits=10, decimal_places=2)
    type_options = (
        ('reg', 'regular'),
        ('adj', 'adjustment'),
    )
    type = models.CharField('Typ', max_length=3, choices=type_options, default = 'adj')

class Time_Entry(models.Model):
    user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default='1')
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    description = models.CharField(max_length=250, default='')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=250) #models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

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
    