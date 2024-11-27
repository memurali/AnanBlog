from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class PublicationAdmin(SummernoteModelAdmin):
    summernote_fields = ('longDescripton',)
    readonly_fields = ['lastUpdated']
    save_as = True

class BookAuthorAdmin(SummernoteModelAdmin):
    summernote_fields = ('bio',)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)

admin.site.register(PublicationCategorie)
admin.site.register(TableOfContent)
admin.site.register(AuthorEducation)
admin.site.register(AuthorCareer)
