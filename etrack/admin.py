from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Express
import datetime
from rangefilter.filter import DateRangeFilter
from django.http import HttpResponse
from import_export.admin import ExportActionMixin
from import_export import resources

# Register your models here.
class MyAdminSite(admin.AdminSite):
    pass

def upload_track_number(modeladmin, request, queryset):
    pass
upload_track_number.short_description = '上传快递单号的Excel文件'


class ExpressResource(resources.ModelResource):
    class Meta:
        model = Express
        



class ExpressAdmin( admin.ModelAdmin):
    def download_excel(self, request, queryset):
        express_resource = ExpressResource()
        dataset = express_resource.export()
        response = HttpResponse(dataset.xls, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=liebaosudi_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d-%H-%M'))
        return response
    download_excel.short_description = '下载已选中的excel文件'

    # disable delete action
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    fieldsets = [
        ('代理人', {'fields':['agent_account',],}),
        ('发件人信息', {'fields':['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop','sender_country','sender_province','sender_city','sender_district','sender_address',],}),
        ('收件人信息', {'fields':['auto_recipient_name', 'recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'recipient_photo']}),
        ('快递信息', {'fields':['track_number', 'packet_state']}),
    ]
    readonly_fields = ('agent_account','sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop','sender_country','sender_province','sender_city','sender_district','sender_address','auto_recipient_name', 'recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'recipient_photo','packet_state')
    list_display = ('sender_wechat_num',  'track_number', 'created_date', 'packet_state')
    list_filter = (('created_date',DateRangeFilter),'packet_state',)
    search_fields = ['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop','recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'track_number','packet_state']
    list_per_page = 20
    actions = [download_excel,]
    

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Express, ExpressAdmin)
