from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Express
import datetime
from rangefilter.filter import DateRangeFilter
from django.http import HttpResponse
from import_export.admin import ImportMixin, ImportForm,ConfirmImportForm
from import_export import resources, fields
from django import forms
from import_export import instance_loaders

class MyAdminSite(admin.AdminSite):
    pass

class ExpressResource(resources.ModelResource):
    class Meta:
        model = Express
        exclude = ('id',)
    def get_export_headers(self):
        headers = []
        for field in self.get_fields():
            model_fields = self.Meta.model._meta.get_fields()
            header = next((x.verbose_name for x in model_fields if x.name == field.column_name), field.column_name)
            headers.append(header)
        print(headers)
        return headers

def get_instance(self, row):
    try:
        params = {}
        for key in self.resource.get_import_id_fields():
            field = self.resource.fields[key]
            params[field.attribute] = field.clean(row)
        if params:
            rs = list(self.get_queryset().filter(**params))
            if len(rs) < 2:
                return self.get_queryset().get(**params)
            return self.get_queryset().filter(**params)[len(rs)-1]
        else:
            return None
    except self.resource._meta.model.DoesNotExist:
        return None
# monkey patch
instance_loaders.ModelInstanceLoader.get_instance = get_instance

class ImportResource(resources.ModelResource):
    track_number = fields.Field(column_name="申通单号", attribute="track_number")
    recipient_id = fields.Field(column_name="收件人身份证", attribute="recipient_id")
    recipient_phone_num = fields.Field(column_name="收件人手机", attribute="recipient_phone_num")
    recipient_name = fields.Field(column_name="收件人姓名", attribute="recipient_name")
    class Meta:
        model = Express
        report_skipped= True
        skip_unchanged = True
        fields = ('track_number','recipient_id','recipient_phone_num', 'recipient_name')
        # import_id_fields = ('recipient_id','track_number')
        import_id_fields = ('recipient_id',)
        exclude = ('id')

    def get_or_init_instance(self, instance_loader, row):
        """
        Either fetches an already existing instance or initializes a new one.
        """
        if not self._meta.force_init_instance:
            instance = self.get_instance(instance_loader, row)
            loacl_track_num = self.get_import_fields()[0].get_value(instance)
            if loacl_track_num and loacl_track_num != row['申通单号']:
                return (self.init_instance(row), True)
            if instance:
                return (instance, False)
        return (self.init_instance(row), True)
        
    def skip_row(self, instance, original):
        if self.get_import_fields()[0].get_value(original) != None:
            return True
        # if str(original) == '-----None-----None':
        #     return True
        return False

class ExpressAdmin(ImportMixin, admin.ModelAdmin):
    # import excel
    
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
    list_display = ('packet_state', 'sender_wechat_num',  'track_number', 'created_date')
    list_filter = (('created_date',DateRangeFilter),'packet_state',)
    search_fields = ['sender_wechat_num','sender_name','sender_wechat_name','sender_mobile_num','shop','recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id', 'track_number','packet_state']
    list_per_page = 20
    actions = [download_excel,]

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return True
        return False
    
    # remove '------' from actions select tag
    def get_action_choices(self, request):
        choices = super(ExpressAdmin, self).get_action_choices(request)
        choices.pop(0)
        return choices

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Express, ExpressAdmin)
