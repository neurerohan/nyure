from django.contrib import admin
from .models import Vegetable

@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_nepali', 'unit', 'min_price', 'max_price', 'avg_price', 'scrape_date')
    list_filter = ('scrape_date', 'name')
    search_fields = ('name', 'name_nepali')
    date_hierarchy = 'scrape_date'