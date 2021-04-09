from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Express
import datetime
from rangefilter.filter import DateRangeFilter
from django.http import HttpResponse
from import_export.admin import ImportMixin
from import_export import resources

class MyAdminSite(admin.AdminSite):
    pass

class ExpressResource(resources.ModelResource):
    class Meta:
        model = Express
        exclude = ('id', 'recipient_photo')
    def get_export_headers(self):
        headers = []
        for field in self.get_fields():
            model_fields = self.Meta.model._meta.get_fields()
            header = next((x.verbose_name for x in model_fields if x.name == field.column_name), field.column_name)
            headers.append(header)
        return headers

class ImportResource(resources.ModelResource):
    class Meta:
        model = Express

class ExpressAdmin(admin.ModelAdmin):
    resource_class = ImportResource
    def download_excel(self, request, queryset):
        express_resource = ExpressResource()
        dataset = express_resource.export()
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=liebaosudi_{}.xlsx'.format(datetime.datetime.now().strftime('%Y%m%d-%H-%M'))
        return response
    download_excel.short_description = '选中并下载excel文件'

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
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_action_choices(self, request):
        choices = super(ExpressAdmin, self).get_action_choices(request)
        choices.pop(0)
        return choices

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Express, ExpressAdmin)
