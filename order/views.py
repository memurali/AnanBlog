from django.shortcuts import render
from django.http import HttpResponse as hre
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from datetime import date
import json
from base.loginReq import login_required
from publications.models import (
    Publication,
    TableOfContent
)

from base.blogContent import getBlogs
from base.publicationContent import getPublication

from base.models import (
    UserInfo,
    MemberShips, 
    Cart
)

from .models import *
from blog.models import *

from base.menuContent import getMenuBlogs


@login_required()
@require_http_methods(["POST"])
def setOrder(request):
    
    if request.method == 'POST':
        orderNumber = request.POST.get("orderNumber", 1)        
        products = json.loads(request.POST.get("products", 1))

        uid = request.user.id
        getUser = User.objects.get(id=uid)

        checkOrder = Order.objects.filter(orderNumber=orderNumber)

        if not checkOrder:
            setOrder = Order.objects.create(
                userId=getUser,
                orderNumber=orderNumber,
                orderStatus="pending",
            )
            setOrder.save()

            for product in products['products']:
                # print(product['product_name'])

                product_id = Publication.objects.get(id=product['product_id'])
                
                OrderItems.objects.create(
                    orderId = setOrder,
                    productID = product_id,
                    productType = product['product_type'],
                    productName = product['product_name'],
                    quantity = product['quantity'],
                    price = product['product_price'],
                )

            chekItem = Cart.objects.filter(userId=getUser)

            if not chekItem:
                pass
            else:
                chekItem.delete()

        print(products['products'])
        return hre("success")

@login_required()
@require_http_methods(["POST"])
def ConfirmOrder(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    orderNumber = request.POST.get("orderNumber", 1)
    context["orderNumber"] = orderNumber

    context["today"] = date.today()

    uid = request.user.id
    getUser = User.objects.get(id=uid)

    if request.user.is_authenticated == True:
        context['loggedin'] = True

    userOrder = Order.objects.get(orderNumber=orderNumber)

    if not userOrder:
        pass
    else:
        userOrderItem = OrderItems.objects.filter(orderId=userOrder)

        context['cartItems'] = userOrderItem

        productItem = 0
        tottalCost = 0
        productPrice = []
        for item in userOrderItem:
            productItem += 1

            productPrice.append({
                "price":item.price*item.quantity,
                "itemId":item.id
            })

            tottalCost += item.price*item.quantity

        context['cartSummary'] = {
            "productItem":productItem,
            "tottalCost": tottalCost,
            "productPrice": productPrice
        }

    return render(request, 'order-confirm.html', context)

def OrderView(request):
    context = {}

    context['menuContent'] = getMenuBlogs()

    context['categories'] = BlogCategorie.objects.all().order_by('category_order')

    uid = request.user.id
    getUser = User.objects.get(id=uid)

    userOrder = Order.objects.filter(userId=getUser).order_by('-id')

    context['orders'] = userOrder

    return render(request, 'order.html', context)