#game_of_live/models.py
from django.db import models
from django.utils import timezone

# python3 manage.py makemigrations game_of_live
# python3 manage.py migrate

# Create your models here.
'''
class Comment(models.Model):
    name = models.CharField(max_length = 20)
    comment = models.TextField()
    date_added = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return '<Name: {}, ID: {}>'.format(self.name, self.id)
'''