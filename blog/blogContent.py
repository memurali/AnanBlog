from .models import *
from django.core.paginator import Paginator
from django.templatetags.static import static
from base.models import UserInfo, Comments, CommentReply
from datetime import datetime

def getSimilarBlogs(category, bgId):

    similar_blogs = Blogs.objects.filter(categories=category).order_by("-id")

    contents = ""

    i = 0

    for bdt in similar_blogs:

        if bdt.id != bgId:

            dTime = bdt.dateAdded.strftime("%d/%m/%y %H:%M")

            i += 1

            if i > 6: 
                break

            contents += f"""

                <div class="col-md-6 article-col">
                  <div class="article-box">
                     <div class="list-number">0{i}</div>
                     <div class="article-content">
                        <h2 class="entry-title"><a href="/articles/details/{bdt.title}-{bdt.id}">{bdt.title}</a></h2>
                        <div class="entry-meta">
                           <div class="date">{dTime}</div>
                        </div>
                        <a href="/articles/details/{bdt.title}-{bdt.id}" class="download-link">Download PDF</a>
                     </div><!-- .article-content -->
                  </div>
               </div>
            
            """

    return contents

def getIndexContent():
    categories = BlogCategorie.objects.all().order_by('category_order')

    contents = ""

    for category in categories:
        
        articles = Blogs.objects.filter(categories=category).order_by('-id')[:3]

        content = f"""
            <div class="row mt-2">
                <div class="col">
                    <div class="row">
                        <h1 class="col-7 col-blog-index text-warning">{category.category_name}</h1><a href="{category.category_slug}" class="sh-all">Show All</a>
                    </div>
                </div>
            </div>
        """

        for article in articles:
            image_url = article.image.url if article.image else ''
            content += f"""

            <div class="row mb-2">
                <div class="col">
                    <div class="card mt-3" style="background-color: #000;">
                        <div class="card-body" style="padding: 0;">
                        <div class="row">
                            <div class="col-8 col-blog-index">
                                <a href="details/{article.title}-{article.id}">
                                    <h1 class="text-light">{article.title} </h1>
                                </a>
                                
                                <p class="mt-3" style="font-size: 16px; font-weight: 400;">
                                    {article.shortDescription}
                                    <a href="details/{article.title}-{article.id}" class="text-warning">see more</a>
                                </p>
                            </div>
                    
                            <div class="col-4 col-blog-index">
                                <img class="blog-index-img" note="blog_image" src="{image_url}" alt="">
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>
                """

        contents += content


    return contents

def getIndexContentCat(catId, page_number):
    categories = BlogCategorie.objects.filter(category_slug=catId)

    contents = ""

    for category in categories:
        
        articles = Blogs.objects.filter(categories=category).order_by('-id')

        content = ""

        paginator = Paginator(articles, 5)

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
                                <a href="details/{article.id}">
                                    <h1 class="text-light">{article.title} </h1>
                                </a>
                                
                                <p class="mt-3" style="font-size: 16px; font-weight: 400;">
                                    {article.shortDescription}
                                    <a href="details/{article.id}" class="text-warning">see more</a>
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


        pagin = """
            <div class="row mt-4" style="margin-bottom: 10rem;">
                <div class="col">
                    <nav aria-label="Page navigation example" style="background-color: #000;">
                        <ul class="pagination">"""
        if page_obj.has_previous():
            
            pagin += f""" 
            <li class="page-item">
                <a class="page-link pg-btn" href="?page={page_obj.previous_page_number()}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
                </a>
            </li>"""

        for i in range(page_obj.paginator.num_pages):
            i += 1
            if i == int(page_number):
                pagin += f'<li class="page-item"><a class="page-link active" href="?page={i}">{i}</a></li>'
            else:
                pagin += f'<li class="page-item"><a class="page-link" href="?page={i}">{i}</a></li>'

        if page_obj.has_next():

            pagin += f"""                            
                    <li class="page-item">
                        <a class="page-link pg-btn" href="?page={page_obj.next_page_number()}" aria-label="Next">
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

def getComments(blog_id):

    comments = Comments.objects.filter(blogId=blog_id).order_by('-id')

    contents = ''

    for comment in comments:

        comment_time = comment.commentTime.strftime("%d/%m/%y %H:%M")

        userinfobj = UserInfo.objects.get(userId = comment.userId.id)
        user_placeholder_image = static('/images/profile/user-place-holder.png')

        try:
            userImage = userinfobj.image.url
        except :
            userImage = user_placeholder_image
        
        contents += f"""
            <div class="comment-wrap">
                  <div class="commenter-img"><img class="img-fluid comment-img" src="{userImage}" alt=""></div>
                  <div class="comment-box">
                      <div class="comment-box-header">
                          <h4 class="commenter-name">{comment.userId.username}</h4>
                          <span class="comment-time">{comment_time}</span>
                      </div>
                      <div class="comment-content">
                          <p>{comment.comment}</p>
                      </div>
                      <div class="comment-action">
                          <a href="#blogId" class="reply-link" cmntId="{comment.id}">Reply</a>
                          <div class="form-group mt-3" id="rep_{comment.id}" style="display: none;">
        """

        comment_reply = CommentReply.objects.filter(commentId=comment)

        for reply in comment_reply:

            userinfobj = UserInfo.objects.get(userId = reply.userId.id)

            try:
                userImage = userinfobj.image.url
            except :
                userImage = user_placeholder_image

            reply_time = reply.commentTime.strftime("%d/%m/%y %H:%M")
            
            contents += f"""
                    <div class="comment-box">
                    <img class="img-fluid comment-img" style="position: absolute;" src="{userImage}" alt="">
                      <div class="comment-box-header" style="margin-left: 70px;">
                          <h4 class="commenter-name">{reply.userId.username}</h4>
                          <span class="comment-time">{reply_time}</span>
                      </div>
                      <div class="comment-content" style="margin-left: 70px;">
                          <p>{reply.comment}</p>
                      </div>
                    </div>
            """

        contents += f"""

                            <input type="text" class="form-control mt-3 replay" id="rp_{comment.id}" placeholder="Leave Your Reply">
                              <button class="btn btn-warning mt-1 btn-sm reply-btn" cmntId="{comment.id}">Reply</button>
                              <span class="text-warning ml-3" id="rpm_{comment.id}"></span>
                        </div>
                    </div>
                </div><!-- .comment-box -->
              </div><!-- .comment-wrap -->
        """

    return contents