from django.contrib import admin

from ..models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('id', 'text')
    list_filter = ('id', 'text')
