from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Express
import datetime
from rangefilter.filter import DateRangeFilter
import csv
from django.http import HttpResponse

# Register your models here.


class MyAdminSite(admin.AdminSite):
    pass

def upload_track_number(modeladmin, request, queryset):
    pass
upload_track_number.short_description = '上传快递单号的Excel文件'

class ExpressAdmin(admin.ModelAdmin):
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        field_human_names = [field.verbose_name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=liebaosudi_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d'))
        writer = csv.writer(response)
        writer.writerow(field_human_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    download_csv.short_description = '下载已选中的CSV文件'

    # disable delete action
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    fieldsets = [
        ('寄件人信息', {'fields':['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop'],}),
        ('收件人信息', {'fields':['recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'recipient_photo']}),
        ('快递信息', {'fields':['track_number', 'packet_state']}),
    ]
    readonly_fields = ('sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','recipient_name', 'shop', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'recipient_photo','packet_state')
    list_display = ('sender_wechat_num',  'track_number', 'created_date', 'packet_state')
    list_filter = (('created_date',DateRangeFilter),'packet_state',)
    search_fields = ['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop','recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'track_number','packet_state']
    list_per_page = 20
    actions = [download_csv, upload_track_number]


admin_site = MyAdminSite(name='myadmin')
admin_site.register(Express, ExpressAdmin)
