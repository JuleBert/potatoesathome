#pic_tagger/views.py
from django.shortcuts import render

# Create your views here.
def pic_tagger(request):
    context = {
        'user': 'User 23'
    }
    return render(request, 'pic_tagger/pic_tagger.html', context)