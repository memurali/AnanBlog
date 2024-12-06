from django.db import models

# Create your models here.
class ServiceCategory(models.Model):
    service_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=300, null=True, blank=True)
    Description = models.TextField(default="NA") 

    class Meta:
        db_table = "tbl_ServiceCategory"


class CaseStudy(models.Model):
    cs_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    CaseStudyName = models.CharField(max_length=300, null=True, blank=True)
    Description = models.TextField(default="NA") 
    Images = models.TextField(default='NA') # Use TextField to store image paths

    class Meta:
        db_table = "tbl_CaseStudy"

    def set_Images(self, image_list):
        self.Images = ','.join(image_list)



class Insights(models.Model):
    insight_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    ServiceHeading = models.CharField(max_length=300, null=True, blank=True)
    Description = models.TextField(default="NA") 
    Preview = models.CharField(max_length=300, null=True, blank=True)
    Buy = models.CharField(max_length=300, null=True, blank=True)
    class Meta:
        db_table = "tbl_Insights"