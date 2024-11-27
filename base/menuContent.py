from blog.models import *

def getMenuBlogs():

    categories = BlogCategorie.objects.all().order_by('category_order')[:2]

    contents = ""

    for category in categories:

        articles = Blogs.objects.filter(categories=category).order_by('-id')[:2]

        content = f"""
            <div class="row post-list">
                <div class="col-xl-5 post-col first-col">
                    <h3 class="navbar-section-title">{category.category_name}</h3>
                """

        try:
            content += f"""
                        <div class="post-box">
                        <div class="post-featured-image"><a href="#">
                            <img class="img-fluid" src="{articles[0].image.url}" alt="">
                        </a></div>
                        <div class="post-content">
                            <h3 class="entry-title"><a href="/articles/details/{articles[0].id}">{articles[0].title}</a></h3>
                        </div>
                        </div><!-- .post-col -->
                    </div>"""
        except :
            pass

        try:

            content += f"""
                    <div class="col-xl-7 post-col">
                        <div class="post-box">
                            <div class="post-featured-image"><a href="#"><img class="img-fluid"
                                        src="{articles[1].image.url}" alt=""></a></div>
                            <div class="post-content">
                                <h3 class="entry-title"><a href="/articles/details/{articles[1].id}">{articles[1].title}</a></h3>
                            </div>
                        </div><!-- .post-col -->
                    </div>
            """
        except :
            pass

        content += "</div><!-- .post-list -->"

        contents += content

    return contents