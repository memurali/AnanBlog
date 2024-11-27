import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse as hre
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.http import FileResponse
from django.contrib.auth.decorators import login_required


from publications.models import (
    Publication
)

from base.models import (
    UserInfo,
    MemberShips
)

from base.menuContent import getMenuBlogs
from blog.models import *

def Login(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    login_redirect = request.GET.get('next', 1)

    if request.user.is_authenticated == True:
        if login_redirect != 1:
            return redirect(login_redirect)
        return redirect('/home')

    context['login_redirect'] = login_redirect

    if request.method == 'POST':

        if request.POST.get('form_type', 1) == 'loginform':
            username = request.POST.get('username', 1)
            password = request.POST.get('password', 1)
            login_redirect = request.POST.get('next', 1)

            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if login_redirect != 1:
                    return redirect(login_redirect)

                return redirect('/profile')
            else:
                context['login_error'] = True

        elif request.POST.get('form_type', 1) == 'signupform':
            username = request.POST.get('username', 1)

            street_address = request.POST.get('street_address', 1)
            city = request.POST.get('city', 1)
            state = request.POST.get('state', 1)
            post_code = request.POST.get('post_code', 1)
            country = request.POST.get('country', 1)

            Address = f" {street_address}, {city}, {state}, {post_code}, {country} "

            email = request.POST.get('email', 1)

            password = request.POST.get('password', 1)
            password_con = request.POST.get('password_con', 1)

            if password != password_con:
                context['pass_no_match'] = True

                return render(request, 'login.html', context)

            if User.objects.filter(username=username).exists():
                context['user_exists'] = True

                return render(request, 'login.html', context)

            
            if User.objects.filter(email=email).exists():
                context['email_exists'] = True

                return render(request, 'login.html', context)

            user = User.objects.create_user(username, email, password)
            user.save()


            user_info = UserInfo.objects.create(
                userId = user,
                address = Address
            )

            user_info.save()

            new_user = authenticate(username=username, password=password)

            auth_login(request, new_user)

            return redirect('/subscription')



    return render(request, 'login.html', context)

def Subscribe(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True
    else:
        return redirect('/home')

    return render(request, 'subscription.html', context)

@require_http_methods(["POST"])
def Congratulation(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    userobj = User.objects.get(id=request.user.id)

    subscriptionID = request.POST.get('subscriptionID', 1)
    orderID = request.POST.get('orderID', 1)
    membershipType = request.POST.get('membershipType', 1)

    createMemberships = MemberShips.objects.create(
        userId = userobj,
        membershipType = membershipType,
        orderID = orderID,
        subscriptionID = subscriptionID
    )

    return render(request, 'congratulation.html', context)

def Profile(request, userid):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    if request.user.is_authenticated == True:
        context['loggedin'] = True
    else:
        return redirect('/home')

    print(userid)

    checkUser = User.objects.filter(username=userid)

    if not checkUser:
        checkUser = User.objects.filter(username__icontains=userid)
        
        if not checkUser:
            context['user_not_exists'] = True

            return render(request, 'profile.html', context)

    uid = checkUser[0].id

    userobj = User.objects.get(id=uid)
    userinfobjChk = UserInfo.objects.filter(userId = uid)

    if not userinfobjChk:
        user_info = UserInfo.objects.create(
                userId = userobj
            )
        user_info.save()
    
    userinfobj = UserInfo.objects.get(userId = uid)

    context['user'] = userobj
    context['user_info'] = userinfobj

    try:
        context['edu_sp'] = userinfobj.education.split("##")
    except:
        context['edu_sp'] = userinfobj.education

    userSubChk = MemberShips.objects.filter(userId = uid)

    if not userSubChk:
        context['user_sub'] = 'free'
    else:
        userSubs = MemberShips.objects.get(userId = uid)
        context['user_sub'] = userSubs.membershipType

    print("address")

    return render(request, 'profile.html', context)


def UProfile(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    uid = request.user.id

    if request.user.is_authenticated == True:
        context['loggedin'] = True
    else:
        return redirect('/home')

    if request.method == 'POST':
        if request.FILES:

            user_info = UserInfo.objects.get(userId=uid)
            user_info.image = request.FILES['file']
            user_info.save()
            
            return hre('success')
        elif request.POST.get('user_name'):
            user_u = User.objects.get(id=uid)
            user_u.username = request.POST.get('user_name', 1)
            user_u.email = request.POST.get('user_email', 1)
            user_u.save()

            user_info = UserInfo.objects.get(userId=uid)
            user_info.address = request.POST.get('user_address', 1)
            user_info.phone = request.POST.get('user_phone', 1)
            user_info.save()

            return hre("success")
        elif request.POST.getlist('fields[]'):

            educations = request.POST.getlist('fields[]')
            education = ''
            for ed in educations:
                education += f"{ed} ## "

            user_mediaAbout = request.POST.get('user_mediaAbout')

            user_info = UserInfo.objects.get(userId=uid)
            user_info.education = education
            user_info.mediaAbout = user_mediaAbout
            user_info.save()

            return hre("success")
        elif request.POST.get('user_facebook'):

            user_info = UserInfo.objects.get(userId=uid)
            user_info.facebook = f"https://www.facebook.com/{request.POST.get('user_facebook', 1)}"
            user_info.twitter = f"https://twitter.com/{request.POST.get('user_twitter', 1)}"
            user_info.linkedin = f"https://www.linkedin.com/in/{request.POST.get('user_linkedin', 1)}"
            user_info.save()

            return hre("success")

        return hre("post request sent")
            

    uid = request.user.id

    userobj = User.objects.get(id=uid)

    userinfobjChk = UserInfo.objects.filter(userId = uid)

    if not userinfobjChk:
        user_info = UserInfo.objects.create(
                userId = userobj
            )
        user_info.save()
    
    userinfobj = UserInfo.objects.get(userId = uid)

    context['user'] = userobj
    context['user_info'] = userinfobj

    try:
        context['edu_sp'] = userinfobj.education.split("##")
    except:
        context['edu_sp'] = ""

    userSubChk = MemberShips.objects.filter(userId = uid)

    if not userSubChk:
        context['user_sub'] = 'free'
    else:
        userSubs = MemberShips.objects.get(userId = uid)
        context['user_sub'] = userSubs.membershipType

    trs = ''
    i = 0

    if context['edu_sp'] == "":
        tr = f'<tr id="row1s">'
        tr += '<td>'
        tr += f'<input class="form-control" name="fields[]" type="text" value="" />'
        tr += '</td>'
        tr += '<td>'
        tr += f'<button class="btn btn-success btn-add" type="button"><span> <i class="fas fa-plus"></i> </span></button>'
        tr += '</td>'

        trs += tr
    else:
        for edu in context['edu_sp']:
            i += 1
            tr = f'<tr id="row{i}s">'

            tr += '<td>'
            tr += f'<input class="form-control" name="fields[]" type="text" value="{edu}" />'
            tr += '</td>'

            if i == 1:
                tr += '<td>'
                tr += f'<button class="btn btn-success btn-add" type="button"><span> <i class="fas fa-plus"></i> </span></button>'
                tr += '</td>'
            else:
                tr += '<td>'
                tr += f'<button id="{i}s" class="btn btn-danger btn-remove" type="button"><span> <i class="fas fa-minus"></i> </span></button></td></tr>'
                tr += '</td>'

            tr += '</tr>'

            trs += tr

    context['trs'] = trs
        

    return render(request, 'profile_user.html', context)

def Logout(request):
    logout(request)

    return redirect('/home')

@login_required
def SecurePub(request, file):
    document = get_object_or_404(Publication, ebookFile=f"publications/{file}")
    path, file_name = os.path.split(file)
    response = FileResponse(document.ebookFile)

    return response