from django.contrib import admin
from .models import Shop
from django.utils.html import format_html

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'address', 'phone', 'whatsapp_number',
        'website', 'start_time', 'end_time', 'personal_courier',
        'round_the_clock', 'image'
    )
    search_fields = ('name', 'address', 'phone', 'whatsapp_number')
    list_filter = ('personal_courier', 'round_the_clock')
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'address', 'phone', 'whatsapp_number', 'description',
                       'website', 'instagram_link', 'facebook_link', 'image')
        }),
        ('Время работы', {
            'fields': ('start_time', 'end_time')
        }),
        ('Дополнительная информация', {
            'fields': ('personal_courier', 'round_the_clock', 'shop_description', 'payment_methods')
        }),
    )
