from django.contrib import admin
from .models import Phone


# Register your models here.


class PhoneAdmin(admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ('name', 'quantity', 'price')


admin.site.register(Phone, PhoneAdmin)
