from django.contrib import admin

from ..models import Target


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'user', 'start_date', 'term', 'is_complete')
    search_fields = ('name', 'category', 'user', 'start_date', 'term')
    list_filter = ('is_complete', 'start_date')
