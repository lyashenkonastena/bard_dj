from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    create_ts = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=400)
    content = models.TextField(blank=True, null=True, verbose_name='text')

    def __str__(self):
        date_str = datetime.strftime(self.create_ts, '%d.%m.%y %H:%M:%S')
        title_short = self.title if len(self.title) <= 30 else self.title[:30] + '…'
        return f'{date_str} {title_short}'
