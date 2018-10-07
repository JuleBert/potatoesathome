#time_tracking/views.py
import datetime

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models.functions import TruncMonth
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .forms import TimeTrackingForm
from .models import Time_Entry

# Create your views here.
def queryset_for_time_list(display_days):
    today_day = datetime.datetime.today()
    return_array = []
    for i in range(display_days,-1,-1):
        reference_day = today_day - datetime.timedelta(days=i)
        the_time_entry = Time_Entry.objects.filter(start_time__date=reference_day)
        if the_time_entry.count() > 0:
            return_array.append(the_time_entry)
    return return_array

class InputView(TemplateView):
    form_class = TimeTrackingForm
    template_name = 'time_tracking/input.html'
    context_object_name = 'latest_time_list'
    initial = {'date':datetime.datetime.now().strftime('%d.%m.%Y'),
                    'end':datetime.datetime.now().strftime('%H:%M'),}
    form = TimeTrackingForm(initial=initial)
    context = {
        'form':form,
        'current_date': datetime.datetime.now().strftime("%d.%m.%Y"),
        'latest_time_list': queryset_for_time_list(5)
    }
    def get(self, request, *args, **kwargs):        
        return render(request,self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            t_e = form.save(commit=False)
            t_e.start_time = datetime.datetime.combine(form.cleaned_data['date'], form.cleaned_data['start'])
            t_e.end_time = datetime.datetime.combine(form.cleaned_data['date'], form.cleaned_data['end'])
            t_e.created_by = request.user
            t_e.created_at = timezone.now()
            t_e.save()
            self.initial = {'date':datetime.datetime.now().strftime('%d.%m.%Y'),
                        'start':form.cleaned_data['end'],
                        #'project':form.cleaned_data['end']
                        }
        t_e = Time_Entry()
        form = TimeTrackingForm(initial=self.initial,instance=t_e)
        self.context['form'] = form
        self.context['latest_time_list'] = queryset_for_time_list(5)
        return render(request, self.template_name, self.context)
    
    #def get_queryset(self):
    #    """Return the last five time entries."""
    #    return Time_Entry.objects.order_by('-start_time')[:5]

class TimeDetailView(DetailView):
    model = Time_Entry
    context_object_name = 'time_entry'
    template_name = 'time_tracking/time_detail.html'

    def get_queryset(self):
        return Time_Entry.objects.filter(id=self.kwargs['pk'])
    
class TimeListView(ListView):
    template_name = 'time_tracking/time_list.html'
    #context_object_name = 'latest_time_list'
    paginate_by = 2
    
    # def get_queryset(self):
    #     """Return the last five time entries."""
    #     return Time_Entry.objects.order_by('-start_time')[:5]

    def get_queryset(self):
        return queryset_for_time_list(100)

    def get_context_data(self, **kwargs):
        context = super(TimeListView, self).get_context_data(**kwargs)
        time_entries = queryset_for_time_list(100)
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

