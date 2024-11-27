from django.shortcuts import render
from django.http import HttpResponse as hre
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from datetime import date
from base.loginReq import login_required
from publications.models import (
    Publication,
    TableOfContent,
    AuthorEducation,
    AuthorCareer,
    BookAuthor
)

import json

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from blog.models import *

from base.createCollage import  genrateCollage

from base.blogContent import (
    getBlogs, 
    getBlogsQuery, 
    getFetured,
    getEducation,
    getCareer,
)

from base.publicationContent import getPublication

from base.models import (
    UserInfo,
    MemberShips,
    Cart,
    ContactUs
)

from order.models import *

from base.menuContent import getMenuBlogs

from constance import config as siteConstance

# Create your views here.
def Home(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order') 

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    context['blogContent'] = getBlogs()

    context["latest_articles"] = Blogs.objects.all().order_by("-id")[:4]
    context["trending_articles"] = Blogs.objects.all().order_by("-viewCount")[:4]
    context["most_shared_articles"] = Blogs.objects.all().order_by("-shareCount")[:4]
    context["featured_articles"] = getFetured()

    bio = BookAuthor.objects.all()[:1]
    if len(bio) > 0:
        context['bio'] = bio[0]
    context['edu'] = getEducation()
    context['career'] = getCareer()

    context['publications'] = Publication.objects.all().order_by("-id")
    
    site_url = request.get_host()

    context["most_shared_articles_graph"] = genrateCollage(Blogs.objects.all().order_by("-shareCount")[:12], site_url)
    context["popular_articles_graph"] = genrateCollage(Blogs.objects.all().order_by("-viewCount")[:12], site_url)
    context["economics_articles_graph"] = genrateCollage(Blogs.objects.filter(categories=2).order_by("-viewCount")[:12], site_url)
    context["business_articles_graph"] = genrateCollage(Blogs.objects.filter(categories=3).order_by("-viewCount")[:12], site_url)

    context['site_url'] = request.get_host()

    return render(request, 'Home.html', context)

def About(request):
    context = {}

    return render(request, 'About.html', context)

def PresentationTemplate(request):
    context = {}

    context['snum'] = [
        {
            "num":1,
            "img":"https://res.cloudinary.com/hj7llsxyl/image/upload/v1633780720/Rectangle_951_yxr1sn.png"
        },
        {
            "num":2,
            "img":"https://res.cloudinary.com/hj7llsxyl/image/upload/v1633775735/sample.jpg"
        },
        {
            "num":3,
            "img":"https://res.cloudinary.com/hj7llsxyl/image/upload/v1631729055/Rectangle_924_j5fsyc.png"
        },
        {
            "num":4,
            "img":"https://res.cloudinary.com/hj7llsxyl/image/upload/v1631729055/Rectangle_930_ujwhwa.png"
        },
        {
            "num":5,
            "img":"https://res.cloudinary.com/hj7llsxyl/image/upload/v1631729055/Rectangle_927_yhrnxq.png"
        },
    ]

    return render(request, 'presentation.html', context)

def Search(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    query = request.GET.get("q", 1)
    page_number = request.GET.get("page", 1)

    if query != 1:
        context['query'] = query
        
        context["searchContent"] = getBlogsQuery(query, page_number)

    return render(request, 'search.html', context)

def allPublication(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    context["publicationContent"] = getPublication()

    return render(request, 'allPublication.html', context)

def publicationDetails(request, pubid):
    context = {}

    pubid = pubid.split("-")[-1]

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    checkPublication = Publication.objects.filter(id=pubid)

    if not checkPublication:
        return redirect('/404')

    publication = Publication.objects.get(id=pubid)

    context['pub'] = publication

    context["page_title"] = publication.title

    biblographics = [
        {"title":"Book Title", "content":publication.title},
        {"title":"eBook ISBN", "content":publication.softcoverISBN},
        {"title":"Number of Pages", "content":publication.numberOfPages},
        {"title":"Book Subtitle", "content":publication.bookSubtitle},
        {"title":"DOI", "content":publication.DOI},
        {"title":"Number of Illustrations", "content":publication.numberOfIllustration},
        {"title":"Authors", "content":publication.authorId},
        {"title":"Softcover ISBN", "content":publication.softcoverISBN},
        {"title":"Topics", "content":publication.topics},
        {"title":"Copyright", "content":publication.copyrightHolder},
        {"title":"Edition Number", "content":publication.editionNumber},
        {"title":"Publisher", "content":publication.publisher},
        {"title":"Copyright Holder", "content":publication.copyrightHolder},
    ]

    context['BiblographicTitles'] = biblographics

    try:
        userobj = User.objects.get(id=request.user.id)

        orders = Order.objects.filter(userId=userobj).filter(orderStatus='com')
    except :
        orders = []

    context['ebookOwned'] = False
    context['hbookOwned'] = False

    for order in orders:

        order_items = OrderItems.objects.filter(productID=publication).filter(productType="ebook")
        order_items_h = OrderItems.objects.filter(productID=publication).filter(productType="hardCover")

        if not order_items:
            pass
        else:
            context['ebookOwned'] = True

        if not order_items_h:
            pass
        else:
            context['hbookOwned'] = True

    tableContents = publication.tableofContents.through.objects.filter(publication_id=pubid)

    contentList = []
    for content in tableContents:
        # print(dir(content))
        TableOfContents = TableOfContent.objects.get(id=content.tableofcontent_id)

        contentDict = {
            "title":TableOfContents.content_title,
            "pages":TableOfContents.pages,
            "price":TableOfContents.price,
            "pubid": pubid,
            "contentOwned": False,
            "file":TableOfContents.contentFile.url,
        }

        for order in orders:

            order_items_c = OrderItems.objects.filter(productName=TableOfContents.content_title).filter(productType="ebook")

            if not order_items_c:
                pass
            else:
                contentDict['contentOwned'] = True

        contentList.append(contentDict)

    context['contents'] = contentList

    return render(request, 'publicationDetails.html', context)

@require_http_methods(["POST"])
def contact_us(request):

    first_name = request.POST.get('first_name', 1)
    last_name = request.POST.get('last_name', 1)
    email = request.POST.get('email', 1)
    phone = request.POST.get('phone', 1)
    consulation = request.POST.get('consulation', 1)
    company_name = request.POST.get('company_name', 1)
    message = request.POST.get('message', 1)
    source = request.POST.get('source', 1)
    additional_details = request.POST.get('additional_details', 1)
    rev_file = request.FILES.get('rev_file', False)

    ContactUs.objects.create(
        firstName=first_name,
        lastName=last_name,
        email=email,
        phone=phone,
        consultation=consulation,
        companyName=company_name,
        message=message,
        additionalDetails=additional_details,
        relevantFile=rev_file if rev_file else None,
        source=source
    )

    context = {}
    context['first_name'] = first_name
    context['last_name'] = last_name
    context['email'] = email
    context['phone'] = phone
    context['consulation'] = consulation
    context['company_name'] = company_name
    context['additional_details'] = additional_details

    html_message = render_to_string("email_template.html", context)
    plain_message = strip_tags(html_message)

    if settings.DEBUG:
        to_email = "vivekcmaurya30@gmail.com"
    else:
        to_email = " anang.tawiah@gmail.com"
    # to_email = "ffries6@gmail.com"

    mail = EmailMessage(
        subject=message,
        body=plain_message,
        to=[to_email],
    )
    if not rev_file:
        pass
    else:
        mail.attach(rev_file.name, rev_file.read(), rev_file.content_type)

    mail.send()

    # send_mail(
    #     subject=message,
    #     message=plain_message,
    #     from_email="Dont Reply <mail@anangtawiah.com>",
    #     recipient_list=[to_email],
    #     html_message=html_message,
    #     fail_silently=False,
    # )

    return redirect('/contact?email_sent=EGAIlz2Vt4')

@require_http_methods(["POST"])
def chkConstance(request):
    
    if request.method == 'POST':
        chkWaterMark = request.POST.get('chkWaterMark', 1)

        if chkWaterMark != 1:

            return hre(siteConstance.WATER_MARK_IMAGES)


# @login_required(next='/all-publications')
@require_http_methods(["POST"])
def SetCartItem(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            productId = request.POST.get('productId', 1)

            nxt = f"next=/publication/details/{productId}"
        else:
            nxt = ""

        return redirect(f"/login?{nxt}")

    getUser = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        productId = request.POST.get('productId', 1)
        productName = request.POST.get('productName', 1)
        productType = request.POST.get('productType', 1)
        price = request.POST.get('price', 1)
        stock = request.POST.get('stock', 0)

        chkItemExists = Cart.objects.filter(userId=getUser).filter(productName=productName).filter(productType=productType).filter(productID=productId)

        if not chkItemExists:

            getProduct = Publication.objects.get(id=productId)
            
            setItems = Cart.objects.create(
                userId = getUser,
                productID = getProduct,
                productName = productName,
                productType = productType,
                price = price,
                stock = stock
            )
            setItems.save()

            return redirect("/cart")

        else:
            return redirect("/cart")

def CartView(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.method == 'POST':

        if request.POST.get("remove_item"):
            itemId =request.POST.get("remove_item")

            chekItem = Cart.objects.filter(id=itemId)

            if not chekItem:
                pass
            else:
                chekItem.delete()

    if request.user.is_authenticated == True:
        context['loggedin'] = True
        
        uid = request.user.id
        getUser = User.objects.get(id=uid)

        userCart = Cart.objects.filter(userId=getUser)
    else:
        userCart = None

    if not userCart:
        context['cartItems'] = False
    else:
        context['cartItems'] = userCart

        productItem = 0
        tottalCost = 0
        productPrice = []
        for item in userCart:
            productItem += 1

            productPrice.append({
                "price":item.price,
                "itemId":item.id
            })

            tottalCost += item.price

        context['cartSummary'] = {
            "productItem":productItem,
            "tottalCost": tottalCost,
            "productPrice": productPrice
        }

    return render(request, 'cart.html', context)

def Privacy(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    return render(request, 'privacy.html', context)

def Terms(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    return render(request, 'terms.html', context)

def ComplaintsPolicy(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    return render(request, 'complaints.html', context)

def Error404(request, exception):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    return render(request, 'error404.html', context)

def My404(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    return render(request, 'error404.html', context)

def Contact(request):
    context = {}

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    email_sent = request.GET.get('email_sent', 1)

    if email_sent == "EGAIlz2Vt4":
        context['email_sent'] = "yes"

    return render(request, 'contact.html', context)

def getCategories(request):

    categories = BlogCategorie.objects.all()

    x = ""

    for category in categories:

        getBlogsNum = Blogs.objects.filter(categories=category)

        x += f"""

            <li>
                <div class="progress-label-bar">
                    <h4 class="progress-label">
                        <a href="/articles/{category.category_slug}">{category.category_name}</a>
                    </h4>
                    <span class="progress-percent">{len(getBlogsNum)}</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width: {len(getBlogsNum)}%" aria-valuenow="{len(getBlogsNum)}" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </li>
        """


    return hre(x)


def getKeywords(request):

    categories = BlogKeyword.objects.all()

    x = ""

    for category in categories:

        getBlogsNum = Blogs.objects.filter(keywords=category)

        x += f"""
            <li>
                <div class="progress-label-bar">
                    <h4 class="progress-label">
                        <a href="/search?q={category.keywords_name}">{category.keywords_name}</a>
                    </h4>
                    <span class="progress-percent">{len(getBlogsNum)}</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width: {len(getBlogsNum)}%" aria-valuenow="{len(getBlogsNum)}" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </li>
        """


    return hre(x)

def getMostPopular(request):

    PopularBlogs = Blogs.objects.all().order_by("-viewCount")[:7]

    i = 1

    poList = []

    for blogs in PopularBlogs:
        podict = {}

        podict['num'] = i
        podict['title'] = blogs.title
        podict['count'] = blogs.viewCount
        podict['id'] = blogs.id

        poList.append(podict)

        i += 1

    return hre(json.dumps(poList))