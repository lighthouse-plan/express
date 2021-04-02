from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Express
import datetime
from rangefilter.filter import DateRangeFilter

# Register your models here.


class MyAdminSite(admin.AdminSite):
    pass





# class CreatedDateFilter(admin.SimpleListFilter):
#     title = _('寄件日期')
#     parameter_name = 'date'
#     def lookups(self, request, model_admin):

#         pass 
#     def queryset(self, request, queryset):
#         pass

class ExpressAdmin(admin.ModelAdmin):
    fieldsets = [
        ('寄件人信息', {'fields':['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop'],}),
        ('收件人信息', {'fields':['recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'recipient_photo']}),
        ('快递信息', {'fields':['track_number', 'packet_state']}),
    ]
    readonly_fields = ('sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','recipient_name', 'shop', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'recipient_photo','packet_state')
    list_display = ('sender_wechat_num',  'track_number', 'created_date')
    list_filter = (('created_date',DateRangeFilter),'packet_state',)
    search_fields = ['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop','recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'track_number','packet_state']
    list_max_show_all = 20

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Express, ExpressAdmin)
