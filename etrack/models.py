from django.db import models
from django.core.validators import RegexValidator

class Express(models.Model):
    class Meta:
        verbose_name = '快递订单'
        verbose_name_plural = "快递订单"
    #寄件人姓名：选填    
    sender_name = models.CharField(max_length=200, null=True, verbose_name="寄件人姓名", blank=True)
    #寄件日期时间
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="寄件日期时间")
    #寄件人微信名字：选填
    sender_wechat_name = models.CharField(max_length=200, null=True, verbose_name="寄件人微信名字", blank=True)
    #寄件人微信号：（必须填写）
    sender_wechat_num = models.CharField(max_length=200, verbose_name="寄件人微信号(必填)", default='0')
    #寄件人手机号码：选填
    mobile_regex = RegexValidator(regex=r'(^0[789]0[0-9]{4}[0-9]{4}$)|^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9]{3})[0-9]{8}$', message="请输入日本或中国手机号码(不加-)")
    sender_mobile_num = models.CharField(validators=[mobile_regex], null=True, max_length=17, verbose_name="寄件人手机号码", blank=True)
    #寄件店铺
    shop = models.CharField(max_length=200, null=True, verbose_name="寄件店铺")

    # 收件人姓名：（必须填写）
    recipient_name = models.CharField(max_length=200, verbose_name="收件人姓名", default='0')
    # 收件人手机号码: （必须填写）
    ch_phone_regex = RegexValidator(regex=r'^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9]{3})[0-9]{8}$', message="请输入中国手机号码")
    recipient_phone_num = models.CharField(max_length=200, validators=[ch_phone_regex], verbose_name="收件人手机号码", default='0')
    # 收件人国家：（中国） 固定
    recipient_country = models.CharField(max_length=200, default='中国', verbose_name="收件人国家")
    # 收件人省：（可选择）
    recipient_province = models.CharField(max_length=200, verbose_name="收件人省", default='0')
    # 收件人市：（可选择）
    recipient_city = models.CharField(max_length=200, verbose_name="收件人市", default='0')
    # 收件人区（县）：（可选择）
    recipient_district = models.CharField(max_length=200, verbose_name="收件人区（县）", default='0')
    # 收件人详细地址：xx省xx市xx区（县）xx号
    recipient_addr = models.CharField(max_length=200, verbose_name="收件人详细地址", default='0')
    # 收件人身份证号码： 
    id_regex = RegexValidator(regex=r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', message="请输入正确的身份证号")
    recipient_id = models.CharField(validators=[id_regex], max_length=200, verbose_name="收件人身份证号码", default='0')
    # 收件人身份证照片上传：建议上传 如遇海关抽查不能及时提交身份证照片出现任何问题我司概不负责
    recipient_photo = models.ImageField(verbose_name="收件人身份证照片上传", blank=True) 

    # 快递单号
    track_number = models.CharField(max_length=200, verbose_name="快递单号", default='xxx', blank=True)

    def __str__(self):
        return self.sender_wechat_num + '-----' + str.split(str(self.created_date), '.')[0]+ '-----' + self.track_number

