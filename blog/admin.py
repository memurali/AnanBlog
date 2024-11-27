from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
from .models import Blogs, BlogCategorie, BlogKeyword
from django_summernote.admin import SummernoteModelAdmin

class BlogsAdmin(SummernoteModelAdmin):
    search_fields = ['title', 'keywords']
    list_filter = ['status', 'categories']
    readonly_fields = ['thumb_image', 'viewCount', 'shareCount', 'dateAdded', 'lastUpdated', 'pdf_file_link']
    save_as = True
    summernote_fields = ('content',)

    fields = [
        'authorId', 'title', 'shortDescription', 'highLights', 'content', 'image', 'thumb_image',
        'categories', 'keywords', 'status', 'viewCount', 'shareCount',
        'dateAdded', 'lastUpdated', 'pdf_file', 'pdf_file_link'
    ]

    def thumb_image(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" id="blogImg" width="250" height="250" />'+
            """
            <script>
            id_image.onchange = evt => {
            const [file] = id_image.files
            if (file) {
                blogImg.src = URL.createObjectURL(file)
            }
            }
            </script>
            """
        )
    thumb_image.short_description = 'Thumbnail'

    def pdf_file_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">View PDF</a> - <a href="{}">Download PDF</a>',
                               obj.pdf_file.url, reverse('admin:download_pdf', args=[obj.id]))
        return "No PDF generated yet."
    pdf_file_link.short_description = 'PDF File'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:id>/download-pdf/', self.admin_site.admin_view(self.download_pdf), name='download_pdf'),
        ]
        return custom_urls + urls

    def download_pdf(self, request, id):
        from django.http import FileResponse
        blog = Blogs.objects.get(id=id)
        if blog.pdf_file:
            return FileResponse(blog.pdf_file.open('rb'), as_attachment=True, filename=f'blog_{id}.pdf')
        else:
            from django.http import HttpResponse
            return HttpResponse("PDF not found", status=404)

admin.site.register(Blogs, BlogsAdmin)
admin.site.register(BlogCategorie)
admin.site.register(BlogKeyword)