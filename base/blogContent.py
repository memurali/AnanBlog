from blog.models import *
from django.core.paginator import Paginator

from publications.models import (
    Publication,
    TableOfContent,
    AuthorEducation,
    AuthorCareer,
    BookAuthor
)

from django.templatetags.static import static

def getCareer():

    edu = BookAuthor.career.through.objects.filter(bookauthor_id=1)

    contents = ""

    for ct in edu:

        ctc = AuthorCareer.objects.get(id=ct.authorcareer_id)
        
        contents += f"""
            <div class="mt-3">
                <p>{ctc.start_year}―Present</p>
                <p style="font-weight: 600;">{ctc.title}</p>
                <p>{ctc.details}</p>
            </div>
        """

    return contents

def getEducation():

    edu = BookAuthor.education.through.objects.filter(bookauthor_id=1)

    contents = ""

    for ct in edu:

        ctc = AuthorEducation.objects.get(id=ct.authoreducation_id)
        
        contents += f"""
            <div class="mt-3">
                <p>{ctc.start_year}―Present</p>
                <p style="font-weight: 600;">{ctc.title}</p>
                <p>{ctc.details}</p>
            </div>
        """

    return contents


def getFetured():

    featured_articles = Blogs.objects.all().order_by("-viewCount")[:4]

    contents = ""

    i = 0

    for arti in featured_articles:

        i += 1

        dt = arti.dateAdded.strftime("%d/%m/%y %H:%M")

        contents += f"""
            <div class='card mt-3' style='background-color: #000;'>
                <div class='card-body' style='padding: 0;'>
                <div class='row'>
                    <div class='col-2'>
                        <h1>{i}</h1>
                    </div>

                    <div class='col-10' style='border-bottom: 1px solid; padding-bottom: 20px;'>
                        <p class='mt-2' style='font-weight: 600; font-size: 15px;'>{dt} | press release</p>
                        
                        <a href="/articles/details/{arti.title}-{arti.id}">
                            <p style='font-size: 18px; margin-top: 25px;'>{arti.title}</p>
                        </a>
                    </div>
                </div>
                </div>
            </div>
        """

    return contents

def getBlogs():
    categories = BlogCategorie.objects.all().order_by('category_order')

    contents = ""

    for category in categories:

        articles = Blogs.objects.filter(categories=category).order_by('-id')[:8]

        content = """
            <div class="row justify-content-center mt-4">
                <div class="col-md-11" style="margin-bottom: 3rem;">
                    <div class="row" style="margin-left: 0;">
        """

        content += f"""
            <div class="col-md-3 col-home-blogs" style="padding: 0;">
                <h1 style="font-size: 44px;
                font-family: 'Montserrat';
                font-weight: 600;
                text-align: left;
                width: 80%;
                " class="col-home-blogs-h1">
                    {category.category_name}
                </h1>
                <a href="articles/{category.category_slug}" class="btn-link" style="font-size: 14px; font-weight: 500; color: #ffc83a !important;">Show All <img note="nowt" src="https://res.cloudinary.com/hj7llsxyl/image/upload/v1631698175/icons/Arrow_7_swft85.png" style="margin-top: -4px;" alt=""></a>
            </div>
        """

        for article in articles:

            keywords = article.keywords.through.objects.filter(blogs_id=article.id)
            keywordsTxt = ", ".join([str(keyword.blogkeyword) for keyword in keywords])

            image_url = article.image.url if article.image else ''

            content += f"""
                <div class="col-md-3 col-home-blogs ml-2 mt-2" style="padding: 0;">
                    <a href="articles/details/{article.title}-{article.id}">
                        <img class="card-img-top" note="blog_image" src="{image_url}" alt="Card image cap">
                        
                        <h4 class="blog-img-title">{article.title}</h4>

                        <span class="blog-img-keywords">
                            <strong>Keywords:</strong> {keywordsTxt}
                        </span>
                    </a>
                </div>
            """

        content += """
                </div>
            </div>
        </div>
        """

        contents += content

    return contents

def getBlogsQuery(query, page_number):

    contents = ""

    articles = Blogs.objects.filter(title__icontains=query).order_by('-id')

    if not articles:
        articles = Blogs.objects.filter(shortDescription__icontains=query).order_by('-id')

        if not articles:
            articles = Blogs.objects.filter(content__icontains=query).order_by('-id')

            if not articles:
                articles = Blogs.objects.filter(categories__category_name__icontains=query).order_by('-id')

                if not articles:
                    articles = Blogs.objects.filter(keywords__keywords_name__icontains=query).order_by('-id')

    content = ""

    paginator = Paginator(articles, 10)

    page_obj = paginator.get_page(page_number)

    for article in page_obj:
        image_url = article.image.url if article.image else ''
        content += f"""

        <div class="row mb-2">
            <dic class="col">
                <div class="card mt-3" style="background-color: #000;">
                    <div class="card-body" style="padding: 0;">
                    <div class="row">
                        <div class="col-8 col-blog-index">
                            <a href="articles/details/{article.title}-{article.id}">
                                <h1 class="text-light">{article.title} </h1>
                            </a>
                            
                            <p class="mt-3" style="font-size: 16px; font-weight: 400;">
                                {article.shortDescription}
                                <a href="articles/details/{article.title}-{article.id}" class="text-warning">see more</a>
                            </p>
                        </div>
                
                        <div class="col-4 col-blog-index">
                            <img class="blog-index-img" note="blog_image" src="{image_url}" alt="">
                        </div>
                    </div>
                    </div>
                </div>
            </dic>
        </div>
            """

    contents += content


    if not articles:
        pass
    else:
        pagin = """
            <div class="row mt-4" style="margin-bottom: 10rem;">
                <div class="col">
                    <nav aria-label="Page navigation example" style="background-color: #000;">
                        <ul class="pagination">"""
        if page_obj.has_previous():
            
            pagin += f""" 
            <li class="page-item">
                <a class="page-link pg-btn" href="?q={query}&page={page_obj.previous_page_number()}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
                </a>
            </li>"""

        for i in range(page_obj.paginator.num_pages):
            i += 1
            if i == int(page_number):
                pagin += f'<li class="page-item"><a class="page-link active" href="?q={query}&page={i}">{i}</a></li>'
            else:
                pagin += f'<li class="page-item"><a class="page-link" href="?q={query}&page={i}">{i}</a></li>'

        if page_obj.has_next():

            pagin += f"""                            
                    <li class="page-item">
                        <a class="page-link pg-btn" href="?q={query}&page={page_obj.next_page_number()}" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                        <span class="sr-only">Next</span>
                        </a>
                    </li>"""

        pagin += """
                    </ul>
                </nav>
            </div>
        </div>
            """

        contents += pagin
                        


    return contents