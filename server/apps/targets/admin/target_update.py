from django.contrib import admin

from ..models import TargetUpdate


@admin.register(TargetUpdate)
class TargetUpdateAdmin(admin.ModelAdmin):
    list_display = ('target', 'amount', 'created_date')
    search_fields = ('target', 'amount', 'created_date')
    list_filter = ('amount', 'created_date')
