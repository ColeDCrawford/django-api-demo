from django.contrib import admin

# Register your models here.
from .models import Amendment

@admin.register(Amendment)
class AmendmentAdmin(admin.ModelAdmin):
    pass