from django.contrib import admin

from .models import BbCodeModel
# Register your models here.

class BbCodeModelAdmin(admin.ModelAdmin):
    list_display = ['pk',]
    list_display_links = ['pk',]

admin.site.register(BbCodeModel, BbCodeModelAdmin)