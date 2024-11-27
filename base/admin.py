from django.contrib import admin
from .models import *

admin.site.site_header = 'Anan Blog Administration'

class MemberShipsAdmin(admin.ModelAdmin):
    readonly_fields = ['userId', 'membershipType', 'orderID', 'subscriptionID', 'dateAdded']

admin.site.register(MemberShips, MemberShipsAdmin)
admin.site.register(ContactUs)
