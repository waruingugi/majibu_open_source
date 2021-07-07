from django.contrib import admin
from core.models import Subscribers
from django.contrib.auth.models import Group


# Register your models here.
class SubscribersPage(admin.ModelAdmin):
    list_display = ('subscribed_date', 'name', 'email')

    search_field = ['name']
    list_filter = ('subscribed_date',)


admin.site.register(Subscribers, SubscribersPage)
admin.site.unregister(Group)
