#time_tracking/models.py
from _datetime import datetime, timedelta, date
import holidays

from django.db import models
from django.utils import timezone
from django.utils.six import with_metaclass
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User as DjangoUser

# python3 manage.py makemigrations time_tracking
# See the SQL:
# python3 manage.py sqlmigrate time_tracking 0001 
# python3 manage.py migrate

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(days=n)

def calc_overtime(settings_entry, reference_date, hours_dec):
    # https://pypi.org/project/holidays/
    de_holidays = holidays.CountryHoliday('DE', prov='SN')
    if (reference_date in de_holidays):
        return hours_dec
    else:
        wd = reference_date.weekday()
        if wd == 0:
            return hours_dec - float(settings_entry.work_time_mon)
        elif wd == 1:
            return hours_dec - float(settings_entry.work_time_tue)
        elif wd == 2:
            return hours_dec - float(settings_entry.work_time_wed)
        elif wd == 3:
            return hours_dec - float(settings_entry.work_time_thu)
        elif wd == 4:
            return hours_dec - float(settings_entry.work_time_fri)
        elif wd == 5:
            return hours_dec - float(settings_entry.work_time_sat)
        elif wd == 6:
            return hours_dec - float(settings_entry.work_time_sun)

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
    project_code = models.CharField('Projektcode', max_length=10)
    project_description = models.CharField('Projektbeschreibung', max_length=100, default = '')
    emp_options = (
        ('KEINE','Keine'),
        ('AVGL', 'Avantgarde-labs'),
        ('CE', 'Conrad'),
    )
    employer = models.CharField('Schnittstelle', max_length=20, choices=emp_options, default = 'KEINE')
    def __str__(self):
        return str(self.project_code) + ' ' + str(self.project_description)

class SettingsModel(models.Model):
    user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default='1')
    created_at = models.DateTimeField(default=timezone.now)
    start_date = models.DateField('Startdatum', default=date(2018,1,1))
    work_time_mon = models.DecimalField('Arbeitszeit Montag', max_digits=10, decimal_places=2, default=8)
    work_time_tue = models.DecimalField('Arbeitszeit Dienstag', max_digits=10, decimal_places=2, default=8)
    work_time_wed = models.DecimalField('Arbeitszeit Mittwoch', max_digits=10, decimal_places=2, default=8)
    work_time_thu = models.DecimalField('Arbeitszeit Donnerstag', max_digits=10, decimal_places=2, default=8)
    work_time_fri = models.DecimalField('Arbeitszeit Freitag', max_digits=10, decimal_places=2, default=8)
    work_time_sat = models.DecimalField('Arbeitszeit Samstag', max_digits=10, decimal_places=2, default=0)
    work_time_sun = models.DecimalField('Arbeitszeit Sonntag', max_digits=10, decimal_places=2, default=0)

class Overtime_Entry(models.Model):
    user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default='1')
    overtime_date = models.DateField('Datum', unique = True)
    reg_overtime = models.DecimalField('Überstunden', max_digits=10, decimal_places=2)
    adj_overtime = models.DecimalField('Überstunden', max_digits=10, decimal_places=2, null=True)

    def get_overtime(self, reference_date, user_id):
        my_overtime = Overtime_Entry.objects.filter(overtime_date=reference_date, user_id=user_id)
        if my_overtime.count() > 0:
            if my_overtime[0].reg_overtime is not None:
                adjustment = 0
                if my_overtime[0].adj_overtime is not None:
                    adjustment = my_overtime[0].adj_overtime
                return my_overtime[0].reg_overtime + adjustment
            else:
                pass
                # TODO
        my_overtime = Overtime_Entry.objects.filter(user_id=user_id).order_by('-overtime_date')
        settings = SettingsModel.objects.filter(user_id=user_id).order_by('-created_at')
        if settings.count() == 0:
            settings = SettingsModel()
            settings.save()
        else:
            settings = settings[0]
        if my_overtime.count() == 0:
            start_range = settings.start_date
        else:
            my_overtime = my_overtime[0]
            start_range = my_overtime.overtime_date + timedelta(days=1)
        if reference_date < start_range:
            return 0
        for single_date in daterange(start_range, reference_date + timedelta(days=1)):
            last_oe = Overtime_Entry.objects.filter(user_id=user_id,overtime_date=single_date+timedelta(-1))
            last_overtime = 0
            if last_oe.count() != 0:
                if last_oe[0].adj_overtime is not None:
                    adjusted = float(last_oe[0].adj_overtime)
                else:
                    adjusted = 0
                last_overtime = float(last_oe[0].reg_overtime) + adjusted
            te = Time_Entry(start_time=datetime.combine(single_date, datetime.min.time()))
            hours_worked = te.get_days_work_hours()
            reg_overtime = calc_overtime(settings, single_date, hours_worked) + last_overtime
            entry = Overtime_Entry(user_id=user_id,overtime_date=single_date,reg_overtime=reg_overtime)
            entry.save()
        return reg_overtime

class Time_Entry(models.Model):
    user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default='1')
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    description = models.CharField(max_length=250, default='')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=250) #models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def get_overtime(self):
        oe = Overtime_Entry()
        return oe.get_overtime(self.start_time.date(), self.user_id)

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
        work_seconds = self.get_days_work_sec()
        return self.format_timedelta(work_seconds)

    def get_days_work_sec(self):
        work_seconds = 0
        for today_entry in Time_Entry.objects.filter(start_time__date=self.start_time.date()):
            # print(today_entry, today_entry.start_time, today_entry.end_time, today_entry.end_time - today_entry.start_time)
            days_work = today_entry.end_time - today_entry.start_time
            work_seconds += days_work.seconds
        return work_seconds

    def get_days_work_hours(self):
        return self.get_days_work_sec() / 3600

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
    