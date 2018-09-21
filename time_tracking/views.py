#time_tracking/views.py
from datetime import datetime

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView

from .forms import TimeTrackingForm
from .models import Time_Entry

# Create your views here.

class InputView(TemplateView):
    form_class = TimeTrackingForm
    template_name = 'time_tracking/input.html'
    context_object_name = 'latest_time_list'
    initial = {'date':datetime.now().strftime('%d.%m.%Y'),
                    'end':datetime.now().strftime('%H:%M'),}
    form = TimeTrackingForm(initial=initial)
    context = {
        'form':form,
        'current_date': datetime.now().strftime("%d.%m.%Y"),
        'latest_time_list':Time_Entry.objects.order_by('-start_time')[:5]
    }
    def get(self, request, *args, **kwargs):        
        return render(request,self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            t_e = form.save(commit=False)
            t_e.start_time = datetime.combine(form.cleaned_data['date'], form.cleaned_data['start'])
            t_e.end_time = datetime.combine(form.cleaned_data['date'], form.cleaned_data['end'])
            t_e.created_by = request.user
            t_e.created_at = timezone.now()
            t_e.save()
            self.initial = {'date':datetime.now().strftime('%d.%m.%Y'),
                        'start':form.cleaned_data['end'],
                        #'project':form.cleaned_data['end']
                        }
        t_e = Time_Entry()
        form = TimeTrackingForm(initial=self.initial,instance=t_e)
        self.context['form'] = form
        return render(request, self.template_name, self.context)
    
    #def get_queryset(self):
    #    """Return the last five time entries."""
    #    return Time_Entry.objects.order_by('-start_time')[:5]

class TimeDetailView(DetailView):
    model = Time_Entry
    template_name = 'time_tracking/time_detail.html'

    
class TimeListView(ListView):
    template_name = 'time_tracking/time_list.html'
    context_object_name = 'latest_time_list'
    
    def get_queryset(self):
        """Return the last five time entries."""
        return Time_Entry.objects.order_by('-start_time')[:5]
