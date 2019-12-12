from django.contrib import admin
from .models import Costume


# Register your models here.


class CostumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price')


admin.site.register(Costume, CostumeAdmin)
