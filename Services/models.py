from django.db import models

# Create your models here.
class ServiceCategory(models.Model):
    service_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=300, null=True, blank=True)
    Description = models.TextField(default="NA") 

    class Meta:
        db_table = "tbl_ServiceCategory"