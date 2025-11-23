from django.db import models

class LeadStatus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = "LeadStatus"
        verbose_name = "LeadStatus"
        verbose_name_plural = "LeadStatus"
        
    def __str__(self):
        return self.status or "Unnamed Status"


class Leads(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    status = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Leads"
        verbose_name = "Leads"
        verbose_name_plural = "Leads"

