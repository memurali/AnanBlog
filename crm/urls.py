from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard),
    path("dashboard", views.Dashboard),
    path("contacts", views.Contacts),
    path("leads", views.Leads),
    path("accounts", views.Accounts),
    path("customer/<int:cid>", views.Customer),
    path("get-activity/<int:cid>", views.getContactActivity),
    path("send-message", views.sent_message),
    path("save-activity", views.save_activity),
    path("invoices", views.Invoices),
    path("invoice/<str:invid>", views.Invoice_details),
    path("send-to-recipient/<str:inv_num>", views.sent_to_recipient),
    path("create-invoice", views.create_invoice),
    path("login", views.Login),
    path("logout", views.Logout),
    path("create-new-sender", views.createNewSender),
    path("create-new-receipt", views.createNewReceipt),
    path("create-new-invoice", views.createNewInvoice),
]