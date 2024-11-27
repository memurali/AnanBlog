from django.db import models
from django.conf import settings
from publications.models import Publication
from blog.models import Blogs

from django.utils.timezone import now


class UserInfo(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='profile')
    address = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=300, null=True, blank=True)
    education = models.CharField(max_length=300, null=True, blank=True)
    mediaAbout = models.CharField(max_length=300, null=True, blank=True)
    facebook = models.CharField(max_length=300,  default="#")
    twitter = models.CharField(max_length=300, default="#")
    linkedin = models.CharField(max_length=300, default="#")
    emailVarified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.userId)

    class Meta:
        db_table = "auth_user_info"

class MemberShips(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membershipType = models.CharField(max_length=300, null=True, blank=True)
    orderID = models.CharField(max_length=300, null=True, blank=True)
    subscriptionID = models.CharField(max_length=300, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.subscriptionID)

class Cart(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    productID = models.ForeignKey(Publication, on_delete=models.CASCADE)
    productName = models.CharField(max_length=300, null=True, blank=True)
    productType = models.CharField(max_length=300, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return str(self.productName)

    class Meta:
        db_table = "tbl_cart"

class Comments(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blogId = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    comment = models.TextField(blank=True,null=True)
    commentTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_comments"

class CommentReply(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commentId = models.ForeignKey(Comments, on_delete=models.CASCADE)
    comment = models.TextField(blank=True,null=True)
    commentTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_comment_reply"

class ContactUs(models.Model):
    firstName = models.CharField(max_length=300, null=True, blank=True)
    lastName = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=300, null=True, blank=True)
    consultation = models.CharField(max_length=300, null=True, blank=True)
    companyName = models.CharField(max_length=300, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    additionalDetails = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=300, default="UnKnown")
    relevantFile = models.FileField(upload_to='contactus_file/', null=True, blank=True)
    createdDate = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return str(self.email)

    class Meta:
        db_table = "tbl_contact_us"