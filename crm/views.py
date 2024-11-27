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
from django.core.mail import send_mail, EmailMessage

from crm.ContactContent import getContact
from crm.LeadsContent import getLeads
from crm.AccountContent import *

from .createInvoice import createInvoice

from base.models import ContactUs
from .models import *

def Dashboard(request):
    context = {}

    context['page_name'] = "dashboard"

    if request.user.is_authenticated != True:
        return redirect('/crm/login')
    elif request.user.is_staff != True:
        return redirect('/crm/login?not_staff')

    context['contacts'] = getContact("5", 0)
    context['leads'] = getLeads("5", 0)

    return render(request, "crm/dashboard.html", context)


def Contacts(request):
    context = {}

    context['page_name'] = "contacts"

    if request.user.is_authenticated != True:
        return redirect('/crm/login')
    elif request.user.is_staff != True:
        return redirect('/crm/login?not_staff')

    context['contacts'] = getContact("all", request.GET.get("page", 1))

    return render(request, "crm/contacts.html", context)

def Leads(request):
    context = {}

    context['page_name'] = "leads"

    if request.user.is_authenticated != True:
        return redirect('/crm/login')
    elif request.user.is_staff != True:
        return redirect('/crm/login?not_staff')

    context['leads'] = getLeads("all", request.GET.get("page", 1))

    return render(request, "crm/leads.html", context)

def Accounts(request):
    context = {}

    context['page_name'] = "accounts"

    if request.user.is_authenticated != True:
        return redirect('/crm/login')
    elif request.user.is_staff != True:
        return redirect('/crm/login?not_staff')

    context['accounts'] = getAccount("all", request.GET.get("page", 1))

    return render(request, "crm/accounts.html", context)


def Invoices(request):
    context = {}

    context['page_name'] = "invoice"

    if request.user.is_authenticated != True:
        return redirect('/crm/login')
    elif request.user.is_staff != True:
        return redirect('/crm/login?not_staff')

    context['invoices'] = Inoice.objects.all().order_by('-id')

    return render(request, "crm/invoices.html", context)

def Invoice_details(request, invid):
    context = {}

    context['page_name'] = "invoice"

    if request.user.is_authenticated != True:
        return redirect('/crm/login')
    elif request.user.is_staff != True:
        return redirect('/crm/login?not_staff')

    context['invoice'] = Inoice.objects.get(invoice_number=invid)

    if context['invoice'].invoice_sender.company_logo == "":
        context['sender_logo'] = False

    context['items'] = invoice_items.objects.filter(invoice_id=context['invoice'].id)

    total = 0
    discounts = context['invoice'].discounts
    taxes = context['invoice'].taxes

    for item in context['items']:
        total += item.amount

    context['total'] = total
    context['total_discounts'] = total * (discounts/100)
    context['total_taxes'] = total * (taxes/100)
    context['sub_total'] = (total - context['total_discounts']) + context['total_taxes']

    print(context['items'])

    return render(request, "crm/invoices-details.html", context)

@require_http_methods(["POST"])
def sent_message(request):
    subject = request.POST.get('subject', 1)
    message = request.POST.get('message', 1)
    to_email = request.POST.get('to_email', 1)
    contact_id = request.POST.get('contact_id', 1)

    # print(subject, message, to_email, contact_id)

    contact = ContactUs.objects.get(id=contact_id)

    SentMessage.objects.create(
        contact_id=contact,
        subject=subject,
        message=message,
        to_email=to_email
    )

    send_mail(
        subject=subject,
        message=message,
        recipient_list=[to_email],
        from_email="Support anangtawiah.com <mail@anangtawiah.com>",
        # html_message=html_message,
        fail_silently=False,
    )

    return hre("success")
    # return hre("Failed")

@require_http_methods(["POST"])
def save_activity(request):
    activity = request.POST.get('activity', 1)
    title = request.POST.get('title', 1)
    description = request.POST.get('description', 1)
    shcedule = request.POST.get('shcedule', 1)
    done = request.POST.get('done', 1)
    contact_id = request.POST.get('contact_id', 1)

    if done == "True":
        done = True
    else:
        done = False

    contact = ContactUs.objects.get(id=contact_id)

    Activities.objects.create(
        contact_id=contact,
        activity=activity,
        title=title,
        description=description,
        schedule=shcedule,
        done=done
    )

    return hre("success")
    # return hre("Failed")

@require_http_methods(["POST"])
def sent_to_recipient(request, inv_num):

    receipt_email = request.POST.get("receipt_email", 1)

    rev_file = f"http://anangtawiah.com/images/invoices/{inv_num}.pdf"
    # rev_file = "https://www.knime.com/sites/default/files/110519_KNIME_Machine_Learning_Cheat%20Sheet.pdf"

    import urllib.request
    response = urllib.request.urlopen(rev_file)

    mail = EmailMessage(
        subject="Invoice From Anangtawah.com",
        body="",
        to=[receipt_email],
    )

    mail.attach(f"{inv_num}.pdf", response.read(), "application/pdf")

    mail.send()
    

    return hre("success")


@require_http_methods(["POST"])
def getContactActivity(request, cid):

    return hre(getActivities(id=cid))

def Customer(request, cid):
    context = {}

    context['page_name'] = "customer"

    if request.user.is_authenticated != True:
        return redirect('/crm/login')
    elif request.user.is_staff != True:
        return redirect('/crm/login?not_staff')

    context["customer"] = ContactUs.objects.get(id=cid)

    context["messages"] = getMessages(id=cid)
    context["activities"] = getActivities(id=cid)

    try:
        context['customer_short'] = context["customer"].firstName[0].capitalize() + context["customer"].lastName[0].capitalize()

        colorChk = ColorLists.objects.filter(alphabet=context["customer"].firstName[0].capitalize())

        if not colorChk:
            context['av_color'] = "crimson"
        else:
            context['av_color'] = colorChk[0].color
    except :
        context['customer_short'] = "C"
        context['av_color'] = "crimson"

    return render(request, "crm/customer.html", context)

def create_invoice(request):
    context = {}

    context['page_name'] = "invoice"

    context['senderInfo'] = senderInfo.objects.all()
    context['receiptInfo'] = receiptInfo.objects.all()

    return render(request, "crm/create-invoices.html", context)

def Login(request):
    context = {}

    if request.user.is_authenticated == True:
        if request.user.is_staff != True:
            pass
        else:
            return redirect('/crm')
    print(request.GET.get('not_staff', 1))
    if request.GET.get('not_staff', 1) != 1:
        context['not_staff'] = True


    if request.method == 'POST':

        if request.POST.get('form_type', 1) == 'loginform':
            username = request.POST.get('username', 1)
            password = request.POST.get('password', 1)

            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)

                return redirect('/crm')
            else:
                context['login_error'] = True

    return render(request, "crm/login.html", context)

def createNewSender(request):

    sender_name = request.POST.get("sender_name", 1)
    street_address = request.POST.get("street_address", 1)
    city = request.POST.get("city", 1)
    state = request.POST.get("state", 1)
    sender_zip = request.POST.get("zip", 1)
    phone = request.POST.get("phone", 1)
    email = request.POST.get("email", 1)
    company_website = request.POST.get("company_website", 1)
    file = request.FILES.get("file", 1)

    chk_sender = senderInfo.objects.filter(sender_name=sender_name)

    if sender_name == 1:
        return hre("nope")

    if not chk_sender:

        new_sender = senderInfo.objects.create(
            sender_name=sender_name,
            street_address=street_address,
            city=city,
            state=state,
            sender_zip=sender_zip,
            phone=phone,
            email=email,
            company_website=company_website
        )

        if file != 1:
            new_sender.company_logo = file
            new_sender.save()


        return hre("success")
    else:
        print("user_exists")
        return hre("user_exists")

def createNewInvoice(request):

    invoice_number = request.POST.get("invoice_number", 1)
    order_number = request.POST.get("order_number", 1)
    invoice_sender = request.POST.get("invoice_sender", 1)
    invoice_receipt = request.POST.get("invoice_receipt", 1)
    due_date = request.POST.get("due_date", 1)
    send_to_receipt = request.POST.get("send_to_receipt", 1)
    discounts = request.POST.get("discount", 1)
    taxes = request.POST.get("taxes", 1)
    item_name = request.POST.getlist("item_name[]", 1)
    qty = request.POST.getlist("qty[]", 1)
    unit_price = request.POST.getlist("unit_price[]", 1)
    amount = request.POST.getlist("amount[]", 1)

    chk_invoice = Inoice.objects.filter(invoice_number=invoice_number)

    if not chk_invoice:
        pass
    else:
        return hre("invoice_exists")

    sender = senderInfo.objects.get(sender_name=invoice_sender)
    receipt = receiptInfo.objects.get(receipt_name=invoice_receipt)

    if taxes == '':
        taxes = 0
    
    if discounts == '':
        discounts = 0

    create_inv = Inoice.objects.create(
        invoice_number=invoice_number,
        order_number=order_number,
        invoice_sender=sender,
        invoice_receipt=receipt,
        due_date=due_date,
        discounts=discounts,
        taxes=taxes,
    )

    i = 0

    for itm in item_name:

        invoice_items.objects.create(
            invoice_id=create_inv,
            item_name=item_name[i],
            qty=qty[i],
            unit_price=unit_price[i],
            amount=amount[i]
        )

        i += 1

    if sender.company_logo == "":
        company_logo = " "
    else:
        company_logo = sender.company_logo.url

    createInvoice(
        
        companyLogo=company_logo,
        inv_num=invoice_number,
        order_num=order_number,

        inv_id=create_inv.id,
        
        )

    rev_file = f"http://anangtawiah.com/images/invoices/{invoice_number}.pdf"
    # rev_file = "https://www.knime.com/sites/default/files/110519_KNIME_Machine_Learning_Cheat%20Sheet.pdf"

    import urllib.request
    response = urllib.request.urlopen(rev_file)

    if send_to_receipt == 'on':

        mail = EmailMessage(
            subject="Invoice From Anangtawah.com",
            body="",
            to=[receipt.email],
        )

        mail.attach(f"{invoice_number}.pdf", response.read(), "application/pdf")

        mail.send()
    

    return hre("success")

def createNewReceipt(request):

    receipt_name = request.POST.get("receipt_name", 1)
    company_name = request.POST.get("company_name", 1)
    street_address = request.POST.get("street_address", 1)
    city = request.POST.get("city", 1)
    state = request.POST.get("state", 1)
    receipt_zip = request.POST.get("zip", 1)
    phone = request.POST.get("phone", 1)
    email = request.POST.get("email", 1)

    chk_sender = receiptInfo.objects.filter(receipt_name=receipt_name)

    if receipt_name == 1:
        return hre("nope")

    if not chk_sender:

        new_sender = receiptInfo.objects.create(
            receipt_name=receipt_name,
            company_name=company_name,
            street_address=street_address,
            city=city,
            state=state,
            receipt_zip=receipt_zip,
            phone=phone,
            email=email,
        )

        return hre("success")
    else:
        print("user_exists")
        return hre("user_exists")

def Logout(request):
    logout(request)

    return redirect('/crm/login')