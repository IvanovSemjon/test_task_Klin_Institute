from django.contrib import admin
from .models import Worker

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'middle_name', 'last_name', 'position', 'email', 'is_active', 'hired_date', 'created_by')
    list_filter = ('is_active', 'position', 'hired_date')
    search_fields = ('first_name', 'middle_name', 'last_name', 'email', 'position')
    list_editable = ('is_active', 'position')
