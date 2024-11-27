from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.utils.functional import lazy
from django.core.validators import FileExtensionValidator

class PublicationCategorie(models.Model):
    category_name = models.CharField(max_length=250, null=False, blank=False)
    category_slug = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        db_table = "tbl_publication_categories"

    def __str__(self):
        return str(self.category_name)

class TableOfContent(models.Model):
    content_title = models.CharField(max_length=250, null=False, blank=False)
    pages = models.CharField(max_length=250, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False, default=0)
    contentFile = models.FileField(upload_to='publications/', validators=[FileExtensionValidator(["pdf"])], default="#")

    class Meta:
        db_table = "tbl_publication_toc"

    def __str__(self):
        return str(self.content_title)

class AuthorEducation(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    details = models.TextField(max_length=250, null=False, blank=False)
    start_year = models.IntegerField(null=False, blank=False)
    end_year = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.title)


class AuthorCareer(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    details = models.TextField(max_length=250, null=False, blank=False)
    start_year = models.IntegerField(null=False, blank=False)
    end_year = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.title)

class BookAuthor(models.Model):
    author_name = models.CharField(max_length=250, null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    education = models.ManyToManyField(AuthorEducation, default='', blank=True)
    career = models.ManyToManyField(AuthorCareer, default='', blank=True)

    class Meta:
        db_table = "tbl_publication_authors"

    def __str__(self):
        return str(self.author_name)

class Publication(models.Model):
    authorId = models.ForeignKey(BookAuthor, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    heading = models.CharField(max_length=250, null=False, blank=False, default='')
    image = models.ImageField(null=False, blank=False, upload_to='publication_images')
    highResCover = models.ImageField(null=True, blank=True, upload_to='publication_images')
    category = models.ForeignKey(PublicationCategorie, on_delete=models.CASCADE, null=False, blank=False)
    publishYear = models.IntegerField(null=False, blank=False)
    shortDescription = models.TextField(max_length=300, null=True, blank=True)
    longDescripton = models.TextField(null=True, blank=True)
    aboutTextbook = models.TextField(null=True, blank=True)
    aboutAuthors = models.TextField(null=True, blank=True)
    tableofContents = models.ManyToManyField(TableOfContent, default='', blank=True)
    priceHardCover = models.IntegerField(null=False, blank=False)
    priceEbook = models.IntegerField(null=False, blank=False)
    stock = models.IntegerField(null=False, blank=False)
    ebookFile = models.FileField(upload_to='publications/', validators=[FileExtensionValidator(["pdf"])], default="")
    bookSubtitle = models.CharField(max_length=300, null=True, blank=True)
    copyrights = models.CharField(max_length=300, null=True, blank=True)
    publisher = models.CharField(max_length=300, null=True, blank=True)
    copyrightHolder = models.CharField(max_length=300, null=True, blank=True)
    DOI = models.CharField(max_length=300, null=True, blank=True)
    softcoverISBN = models.CharField(max_length=300, null=True, blank=True)
    editionNumber = models.CharField(max_length=300, null=True, blank=True)
    numberOfPages = models.IntegerField(null=False, blank=False)
    numberOfIllustration = models.IntegerField(null=False, blank=False)
    topics = models.CharField(max_length=300, null=True, blank=True)
    status_choices = (
            ('pub', 'Published'),
            ('daf', 'Draft'),
            ('trs', 'Trash'),
        )
    status = models.CharField(max_length=50, choices=status_choices, default='pub')
    lastUpdated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "tbl_publication"

    def __str__(self):
        return str(self.title)

@receiver(post_delete, sender=Publication)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

