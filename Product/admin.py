from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','image', 'model', 'country', 'price', 'category','specifications','store_name')
    search_fields = ('name', 'model', 'country')
    list_filter = ('category',)
