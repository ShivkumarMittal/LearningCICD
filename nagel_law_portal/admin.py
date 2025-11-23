from django.contrib import admin
from .models import forms, category, upload_file


class Registration(admin.ModelAdmin):
    list_display = ('name', 'category', 'link', 'created_at', 'updated_at',)
    ordering = ['-updated_at']

admin.site.register(forms, Registration)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'created_at', 'updated_at',)
    ordering = ['-updated_at']

admin.site.register(category, CategoryAdmin)


class UploadFile(admin.ModelAdmin):
    list_display = ('file_name', 'uploaded_file', 'uploaded_at',)
    ordering = ['-uploaded_at']

admin.site.register(upload_file, UploadFile)