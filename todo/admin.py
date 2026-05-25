from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
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
        'user',
    )

    search_fields = (
        'title',
        'description',
        'user__username',
    )

    ordering = (
        'status',
        '-is_favorite',
        'deadline',
    )
