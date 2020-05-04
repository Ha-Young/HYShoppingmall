from django.contrib import admin
from .models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('hyuser', 'product', 'quantity', 'registered_dttm')

admin.site.register(Order, OrderAdmin)