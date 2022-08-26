from django.contrib import admin

from ..models import TransactionCategory


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    list_filter = ('name',)
    search_fields = ('name', 'user')
