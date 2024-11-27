from django.urls import path
from base.views import commonViews
from base.views import authViews

urlpatterns = [
    #common urls
    path('', commonViews.Home),
    path('home', commonViews.Home),
    path('search', commonViews.Search),
    path('all-publications', commonViews.allPublication),
    path('publication/details/<str:pubid>', commonViews.publicationDetails),
    path('cart', commonViews.CartView),
    path('presentation', commonViews.PresentationTemplate),
    path('about', commonViews.About),
    path('contact', commonViews.Contact),
    path('set-cart', commonViews.SetCartItem),
    path('get-category', commonViews.getCategories),
    path('get-keywords', commonViews.getKeywords),
    path('get-constance', commonViews.chkConstance),
    path('get-most-popular', commonViews.getMostPopular),
    path('set-contact', commonViews.contact_us),
    path('privacy-policy', commonViews.Privacy),
    path('terms-of-use', commonViews.Terms),
    path('complaints-policy', commonViews.ComplaintsPolicy),
    path('404', commonViews.My404),
    
    #userauth urls
    path('login', authViews.Login),
    path('logout', authViews.Logout),
    path('profile/<str:userid>', authViews.Profile),
    path('profile', authViews.UProfile),
    path('subscription', authViews.Subscribe),
    path('thank-you', authViews.Congratulation),
    path('images/publications/<str:file>', authViews.SecurePub),

]
