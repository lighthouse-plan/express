from django.contrib import admin

from .models import Express

# Register your models here.


class MyAdminSite(admin.AdminSite):
    pass

class ExpressAdmin(admin.ModelAdmin):
    fieldsets = [
        ('寄件人信息', {'fields':['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num'],}),
        ('收件人信息', {'fields':[]}),
        ('快递单号', {'fields':['track_number']}),
    ]
    readonly_fields = ('sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num',)
    list_display = ('sender_wechat_num',  'track_number', 'created_date')
    list_filter = ['sender_wechat_num', 'created_date', 'recipient_phone_num']
    search_fields = ['sender_wechat_num', 'recipient_phone_num', 'track_number']
    list_max_show_all = 20

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Express, ExpressAdmin)
