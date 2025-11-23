from django.db import models


class forms(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey('category', on_delete=models.SET_NULL, null=True, blank=True)
    link = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "forms"
        verbose_name = "form"
        verbose_name_plural = "forms"
        

class category(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"
        verbose_name = "category"
        verbose_name_plural = "categories"
       
    def __str__(self):
        return self.category
    
    
class upload_file(models.Model):
    file_name = models.CharField(max_length=255, null=True, blank=True)
    uploaded_file =  models.FileField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "upload_file"
        verbose_name = "upload file"
        verbose_name_plural = "uploaded files"