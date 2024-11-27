from django.db import models
from django.conf import settings
from publications.models import Publication

# Create your models here.

class Order(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orderNumber = models.CharField(max_length=300, null=True, blank=True)
    status_choices = (
            ('pen', 'Pending'),
            ('com', 'Completed'),
        )
    orderStatus = models.CharField(max_length=300, choices=status_choices, default='pen')
    orderDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orderNumber)

    class Meta:
        db_table = "tbl_order"

class OrderItems(models.Model):
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    productID = models.ForeignKey(Publication, on_delete=models.CASCADE)
    productType = models.CharField(max_length=300, null=True, blank=True)
    productName = models.CharField(max_length=300, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.productID)

    class Meta:
        db_table = "tbl_order_items"