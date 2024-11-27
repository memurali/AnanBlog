from blog.models import *
from django.templatetags.static import static

def genrateCollage(model, site_url):

    w = '<div class="info-graph-column">'
    x = '<div class="info-graph-column">'
    y = '<div class="info-graph-column">'
    z = '<div class="info-graph-column">'

    i = 0

    if "127.0.0.1" in site_url or "localhost" in site_url:
        site_url = f"http://{site_url}"
    else:
        site_url = f"https://{site_url}"

    for a in model:
        i += 1
        image_url = a.image.url if a.image else ''
        
        b = f'<img src="{image_url}" note="blog_image" img_url="{site_url}{image_url}" data-toggle="modal" data-target="#graphicsShareModal" class="info-graph-share" title="{a.title}" short_description="{a.shortDescription}" >'

        if i == 1:
            w += b
        elif i == 2:
            x += b
        elif i == 3:
            y += b
        elif i == 4:
            z += b
        elif i == 5:
            w += b
        elif i == 6:
            x += b
        elif i == 7:
            y += b
        elif i == 8:
            z += b
        elif i == 9:
            w += b
        elif i == 10:
            x += b
        elif i == 11:
            y += b
        elif i == 12:
            z += b

    
    w += '</div>'
    x += '</div>'
    y += '</div>'
    z += '</div>'

    m = w + x + y + z

    return m
