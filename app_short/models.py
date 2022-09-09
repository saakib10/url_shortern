from datetime import datetime,timedelta
from django.db import models

from .utils import create_shortened_url

class Shortener(models.Model):
    STATUS_LIST = [
        ('enable','ENABLE'),
        ('disable', 'DISABLE')
    ]


    creation = models.DateTimeField(auto_now_add=True)

    times_followed = models.PositiveIntegerField(default=0)    

    long_url = models.CharField(max_length=500, blank=True)

    short_url = models.CharField(max_length=15, unique=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_LIST, default='enable')
    
    active_time = models.DateTimeField(default=datetime.now())

    class Meta:

        ordering = ["-creation"]


    def __str__(self):

        return f'{self.long_url} to {self.short_url}'

    def save(self, *args, **kwargs):

        # If the short url wasn't specified
        if not self.short_url:
            # We pass the model instance that is being saved
            self.short_url = create_shortened_url(self)
            current_time = datetime.now()
            self.active_time = current_time + timedelta(minutes=10)

        super().save(*args, **kwargs)