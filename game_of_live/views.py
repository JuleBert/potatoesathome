# game_of_live/views.py
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.conf import settings
from .forms import GameOfLiveForm
from .gol.GameofLive import GameOfLife
# Create your views here.


    
class IndexView(TemplateView):
    form_class = GameOfLiveForm
    template_name = 'game_of_live/gol.html'
    #context_object_name = 'latest_time_list'
    initial = {'size': '512',
               'square_size': 8,
               'steps':20,
               'type_1':'hwss',
               'x_position_1': 20,
               'y_position_1': 10,
               'type_2':'giant',
               'x_position_2': 50,
               'y_position_2': 50,
               }
    file_path = os.path.join(settings.MEDIA_ROOT, 'game.gif')
    file_name = 'game.gif'
    form = GameOfLiveForm(initial=initial)
    context = {
        'form':form,
        'gif_name':file_name,
    }
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            figures = [[form.cleaned_data['type_1'], (form.cleaned_data['x_position_1'], form.cleaned_data['y_position_1'])],
                       [form.cleaned_data['type_2'], (form.cleaned_data['x_position_2'], form.cleaned_data['y_position_2'])],
                       ]
            gol = GameOfLife(int(form.cleaned_data['size']), form.cleaned_data['square_size'])
            gol.create_gif(figures=figures, steps=form.cleaned_data['steps'], filename=self.file_path)
            self.context['form'] = form
        return render(request, self.template_name, self.context)