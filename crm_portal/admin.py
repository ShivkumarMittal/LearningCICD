from django.contrib import admin
from crm_portal.models import LeadStatus, Leads

class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    
admin.site.register(LeadStatus, LeadStatusAdmin)

class LeadsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'status', 'tags', 'created_at', 'updated_at')
    ordering = ['-updated_at']
    
admin.site.register(Leads, LeadsAdmin)