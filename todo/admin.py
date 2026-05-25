from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status',
        'priority',
        'category',
        'deadline',
        'is_favorite',
        'created_at',
    )
    list_filter = (
        'status',
        'priority',
        'category',
        'is_favorite',
        'created_at',
    )
    search_fields = (
        'title',
        'description',
    )
    ordering = (
        'status',
        '-is_favorite',
        'deadline',
    )
