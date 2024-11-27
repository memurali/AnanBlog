from django.db import models
from base.models import ContactUs

class ColorLists(models.Model):
    alphabet = models.CharField(max_length=1, null=False, blank=False)
    color = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        db_table = "tbl_color_lists"


class Activities(models.Model):
    contact_id = models.ForeignKey(ContactUs, on_delete=models.CASCADE)
    activity = models.CharField(max_length=200, null=False, blank=False)
    title = models.CharField(max_length=300, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    schedule = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)

    class Meta:
        db_table = "tbl_crm_activities"


class SentMessage(models.Model):
    contact_id = models.ForeignKey(ContactUs, on_delete=models.CASCADE)
    subject = models.CharField(max_length=400, null=False, blank=False)
    message = models.TextField(null=True, blank=True)
    to_email = models.CharField(max_length=300, null=False, blank=False)
    cratedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_crm_sent_message"


class senderInfo(models.Model):
    sender_name = models.CharField(max_length=400, null=False, blank=False)
    street_address = models.CharField(max_length=400, null=False, blank=False)
    city = models.CharField(max_length=400, null=False, blank=False)
    state = models.CharField(max_length=400, null=False, blank=False)
    sender_zip = models.CharField(max_length=400, null=False, blank=False)
    phone = models.CharField(max_length=400, null=False, blank=False)
    email = models.CharField(max_length=400, null=False, blank=False)
    company_website = models.CharField(max_length=400, null=True, blank=True)
    company_logo = models.ImageField(null=True, blank=True, upload_to='crm/sender')

    class Meta:
        db_table = "tbl_crm_invoice_senders"


class receiptInfo(models.Model):
    receipt_name = models.CharField(max_length=400, null=False, blank=False)
    company_name = models.CharField(max_length=400, null=True, blank=True)
    street_address = models.CharField(max_length=400, null=False, blank=False)
    city = models.CharField(max_length=400, null=False, blank=False)
    state = models.CharField(max_length=400, null=False, blank=False)
    receipt_zip = models.CharField(max_length=400, null=False, blank=False)
    phone = models.CharField(max_length=400, null=False, blank=False)
    email = models.CharField(max_length=400, null=False, blank=False)

    class Meta:
        db_table = "tbl_crm_invoice_receipt"

class Inoice(models.Model):
    invoice_number = models.CharField(max_length=150, null=False, blank=False)
    order_number = models.CharField(max_length=150, null=True, blank=True)
    invoice_sender = models.ForeignKey(senderInfo, on_delete=models.CASCADE)
    invoice_receipt = models.ForeignKey(receiptInfo, on_delete=models.CASCADE)
    due_date = models.DateField(auto_now=False)
    cratedAt = models.DateField(auto_now_add=True)
    discounts = models.IntegerField(default=0)
    taxes = models.IntegerField(default=0)

    class Meta:
        db_table = "tbl_crm_invoices"

class invoice_items(models.Model):
    invoice_id = models.ForeignKey(Inoice, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=300, null=False, blank=False)
    qty = models.IntegerField(null=False, blank=False)
    unit_price = models.FloatField(null=False, blank=False)
    amount = models.FloatField(null=False, blank=False)

    class Meta:
        db_table = "tbl_crm_invoices_items"