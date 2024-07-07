from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_email', 'contact_phone')
    search_fields = ('name',)
    filter_horizontal = ('users',)  # Для удобного выбора пользователей

admin.site.register(Company, CompanyAdmin)