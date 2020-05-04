from django.contrib import admin
from .models import Hyuser

# Register your models here.


class HyuserAdmin(admin.ModelAdmin):
    list_display=('email', 'registered_dttm')

admin.site.register(Hyuser, HyuserAdmin)