#time_tracking/views.py
import datetime

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models.functions import TruncMonth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .forms import TimeTrackingForm, NewProjectForm, SettingsForm, OvertimeForm
from .models import Time_Entry, SettingsModel, Overtime_Entry


def queryset_for_time_list(display_days, user_id):
    today_day = datetime.datetime.today()
    return_array = []
    for i in range(display_days,-1,-1):
        reference_day = today_day - datetime.timedelta(days=i)
        the_time_entry = Time_Entry.objects.filter(start_time__date=reference_day, user_id=user_id)
        if the_time_entry.count() > 0:
            return_array.append(the_time_entry)
    return return_array


@method_decorator(login_required, name='dispatch')
class InputView(TemplateView):
    form_class = TimeTrackingForm
    template_name = 'time_tracking/input.html'
    context_object_name = 'latest_time_list'
    initial = {'date': datetime.datetime.now().strftime('%d.%m.%Y'),
               'end': datetime.datetime.now().strftime('%H:%M'), }
    form = TimeTrackingForm(initial=initial)
    context = {
        'form':form,
        'current_date': datetime.datetime.now().strftime("%d.%m.%Y"),
    }

    def get(self, request, *args, **kwargs):
        self.context['latest_time_list'] = queryset_for_time_list(5, self.request.user.id)
        return render(request,self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            t_e = form.save(commit=False)
            t_e.start_time = datetime.datetime.combine(form.cleaned_data['date'], form.cleaned_data['start'])
            t_e.end_time = datetime.datetime.combine(form.cleaned_data['date'], form.cleaned_data['end'])
            t_e.created_by = request.user.username
            t_e.created_at = timezone.now()
            t_e.user_id = request.user
            t_e.save()
            self.initial = {'date':datetime.datetime.now().strftime('%d.%m.%Y'),
                        'start':form.cleaned_data['end'],
                        #'project':form.cleaned_data['end']
                        }
        t_e = Time_Entry()
        form = TimeTrackingForm(initial=self.initial,instance=t_e)
        self.context['form'] = form
        self.context['latest_time_list'] = queryset_for_time_list(5, self.request.user.id)
        return render(request, self.template_name, self.context)

@method_decorator(login_required, name='dispatch')
class Overtime(TemplateView):
    form_class = OvertimeForm
    template_name = 'time_tracking/overtime.html'
    context_object_name = 'overtime_list'

    def get(self, request, *args, **kwargs):
        form = TimeTrackingForm()

        try:
            overtime_list = Overtime_Entry.objects.order_by('-overtime_date')[:10]
        except Overtime_Entry.DoesNotExist:
            overtime_list = None
        context = {
            'form': form,
            'overtime_list': overtime_list
        }
        return render(request,self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            o_entry = form.save(commit=False)
            o_entry.type = 'adj'
            o_entry.user_id = request.user
            o_entry.save()
        o_entry = Overtime_Entry()
        form = OvertimeForm(instance=o_entry)
        context = {
            'form': form,
            'overtime_list': Overtime_Entry.objects.order_by('-overtime_date')[:10]
        }
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class NewProject(TemplateView):
    form_class = NewProjectForm
    initial={
        'project_code':'DATA-',
        'employer': 'CE'
             }
    template_name = 'time_tracking/new_project.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.user_id = request.user
            new_project.save()
            return HttpResponseRedirect('')
            # return redirect('time_tracking:input')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class SettingsView(TemplateView):
    form_class = SettingsForm
    template_name = 'time_tracking/settings.html'
    def get(self, request, *args, **kwargs):
        try:
            instance = SettingsModel.objects.latest('created_at')
        except SettingsModel.DoesNotExist:
            instance = None
        form = self.form_class(instance=instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.user_id = request.user
            settings.save()
            return redirect('time_tracking:input')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class TimeDetailView(DetailView):
    model = Time_Entry
    context_object_name = 'time_entry'
    template_name = 'time_tracking/time_detail.html'

    def get_queryset(self):
        return Time_Entry.objects.filter(id=self.kwargs['pk'])

@method_decorator(login_required, name='dispatch')
class TimeListView(ListView):
    template_name = 'time_tracking/time_list.html'
    paginate_by = 10

    def get_queryset(self):
        return queryset_for_time_list(365, self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(TimeListView, self).get_context_data(**kwargs)
        time_entries = queryset_for_time_list(365, self.request.user.id)
        paginator = Paginator(time_entries, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_entries = paginator.page(page)
        except PageNotAnInteger:
            file_entries= paginator.page(1)
        except EmptyPage:
            file_entries = paginator.page(paginator.num_pages)

        context['latest_time_list'] = file_entries
        return context

