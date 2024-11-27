from publications.models import *

def getPublication():
    categories = PublicationCategorie.objects.all().order_by('id')

    contents = ""

    for category in categories:

        publications = Publication.objects.filter(category=category).order_by('-id')

        if not publications:
            pass
        else:
            
            content = f"""
                <div class="row mt-10">
                <div class="col col-no-pad">
                    <h3 style="font-size: 30px; font-weight: 600;" class="pub-index-h3">{category.category_name}</h3>
                </div>
                </div>

                <div class="row mt-2">
            """

            for publication in publications:

                content += f"""
                    <div class="col-md-3 pub-index-sep">
                    <a href="publication/details/{publication.title}-{publication.id}">
                        <img src="{publication.image.url}"  note="blog_image" alt="" class="pub-img">
                        <h3 style="font-size: 26px; font-weight: 500; margin-top:1rem;">{publication.title}</h3>
                    </a>

                    <p><strong>Format </strong> <span>eBook, Hardcover</span> </p>

                    <p>
                    <strong>From </strong>
                    <span style="font-size: 38px; font-weight: 500; margin-left: 10px;">$ {publication.priceHardCover}</span> 
                    </p>
                </div>
                """

            content += "</div>"

            contents += content

    return contents