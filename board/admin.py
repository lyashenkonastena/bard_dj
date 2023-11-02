from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Ad, Category, Reply


class AdAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Ad, AdAdmin)
admin.site.register(Category)
admin.site.register(Reply)
