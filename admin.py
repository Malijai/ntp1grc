from django.contrib import admin
from .models import Personnegrc


class Personnentp1Admin(admin.ModelAdmin):
    admin.site.site_header = 'Personnes GRC NTP1'
    list_display = ('codeGRC', 'ferme','RA')
    list_filter = ['province', 'ferme', 'RA', 'codeGRC']

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Personnegrc, Personnentp1Admin)