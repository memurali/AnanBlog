from django.shortcuts import render, get_object_or_404
from .models import *
from .blogContent import (
    getIndexContent, 
    getIndexContentCat, 
    getComments,
    getSimilarBlogs
)
from base.models import UserInfo, Comments, CommentReply
from django.http import HttpResponse as hre, FileResponse

from base.menuContent import getMenuBlogs
from django.templatetags.static import static

# Create your views here.

def blogIndex(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    context['content'] = getIndexContent()

    return render(request, "blogIndex.html", context)

def blogIndexCat(request, catid):
    context = {'menuContent': getMenuBlogs(), 'categories': BlogCategorie.objects.all().order_by('category_order')}

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    page_number = request.GET.get('page', 1)

    categoriesChk = BlogCategorie.objects.filter(category_slug=catid)

    if not categoriesChk:
        context['content'] = "<h3>No Data Found</h3>"
    else:
        context['category'] = BlogCategorie.objects.get(category_slug=catid)

        context["page_title"] = context['category'].category_name

        context['content'] = getIndexContentCat(catid, page_number)

    return render(request, "blogIndexCat.html", context)

def articleDetails(request, blogid):
    context = {}
    
    if blogid.isdigit() == False:
        blogid = request.build_absolute_uri().split("-")[-1]

    context['menuContent'] = getMenuBlogs()

    context["trending_articles"] = Blogs.objects.all().order_by("-viewCount")[:5]

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    user_placeholder_image = static('/images/profile/user-place-holder.png')
    context['userImage'] = user_placeholder_image

    if request.user.is_authenticated == True:
        context['loggedin'] = True

        try:
            userinfobj = UserInfo.objects.get(userId = request.user.id)
            context['userInfo'] = userinfobj
            context['userImage'] = userinfobj.image.url
        except :
            context['userImage'] = user_placeholder_image

    blogDt = Blogs.objects.get(id=blogid)

    if request.method == 'POST':
        add_comment = request.POST.get("add_comment", 1)
        get_comment = request.POST.get("get_comment", 1)
        add_reply = request.POST.get("add_reply", 1)
        add_share = request.POST.get("add_share", 1)

        if add_comment != 1:
            comment = request.POST.get("comment", 1)

            Comments.objects.create(
                userId = request.user,
                blogId = blogDt,
                comment = comment
            )

            return hre("success")

        if get_comment != 1:
            blogId = request.POST.get("blogId", 1)

            return hre(getComments(blogId))

        if add_share != 1:
            
            blogDt.shareCount = int(blogDt.shareCount) + 1
            blogDt.save()

            return hre("success")

        if add_reply != 1:
            reply = request.POST.get("reply", 1)
            commentId = request.POST.get("commentId", 1)

            comment = Comments.objects.get(id=commentId)

            CommentReply.objects.create(
                userId = request.user,
                commentId = comment,
                comment = reply
            )

            return hre("success")

    context["blog_comments"] = getComments(blogDt.id)
    
    context["blogDt"] = blogDt

    context["page_title"] = blogDt.title

    context["site_url"] = request.build_absolute_uri()

    keywords = blogDt.keywords.through.objects.filter(blogs_id=blogid)

    context['keywords'] = ''
    for keyword in keywords:
        # print(dir(keyword))
        # print(keyword.blogkeyword, "||", keyword.blogs)
        context['keywords'] += f'<li><a href="/search?q={keyword.blogkeyword}"># {keyword.blogkeyword}</a></li>'

    if blogDt.viewCount is None:
        blogDt.viewCount = 1
        blogDt.save()
    else:
        blogDt.viewCount = int(blogDt.viewCount) + 1
        blogDt.save()

    context["similar_blogs"] = getSimilarBlogs(blogDt.categories, blogDt.id)

    return render(request, "blogDetails.html", context)

def download_blog_pdf(request, blog_id):
    blog = get_object_or_404(Blogs, id=blog_id)
    if blog.pdf_file:
        response = FileResponse(blog.pdf_file.open('rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{blog.title}.pdf"'
        return response
    else:
        return hre('PDF not found', status=404)
