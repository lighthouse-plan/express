from django.db import models
from django.core.validators import RegexValidator
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings

 
""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender,instance,field,instance_file_field)
            
""" Delete the file if something else get uploaded in its place"""

@receiver(pre_save)
def delete_files_when_file_changed(sender,instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            #its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db,field.name)
            instance_file_field = getattr(instance,field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender,instance,field,instance_in_db_file_field)

""" Only delete the file if no other instances of that model are using it"""    
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

def user_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"recipient_photo/{instance.created_date.strftime('%Y')}/{instance.created_date.strftime('%m')}/{instance.created_date.strftime('%d')}/{instance.recipient_name}_{instance.recipient_id}/{instance.created_date}.{str.split(str(filename), '.')[-1]}"


def edit_photo_before_save(image):
    photo = Image.open(image)
    photo = photo.convert('RGBA')
    maxsize = (512, 512)
    photo.thumbnail(maxsize, Image.ANTIALIAS)
    width, height = photo.size

    try: 
        txt_img = Image.new("RGBA", (700,700), (255,255,255,0))
        draw = ImageDraw.Draw(txt_img)
        text = "仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用 \n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用\n\n仅供清关使用 仅供清关使用 仅供清关使用 仅供清关使用"
        try:
            font = ImageFont.truetype(str(settings.STATIC_ROOT)+'/font/STHeiti Medium.ttc', 50)
        except:
            print("error here2")
        textwidth, textheight = draw.textsize(text, font)
        x = 0
        y = 0
        draw.text((x, y), text=text, font=font, fill=(255, 255, 255, 150))
        txt_img = txt_img.rotate(30).crop((10, 100, width + 10, height + 100))
        try:
            photo = Image.alpha_composite(photo, txt_img)
        except:
            print("error here3")
    except:
        print("error here1")

    thumb_io = BytesIO() # create a BytesIO object
    photo = photo.convert('RGB')
    photo.save(thumb_io, 'JPEG', quality=85) 
    thumbnail = File(thumb_io, name=image.name)
    return thumbnail

class Express(models.Model):
    class Meta:
        verbose_name = '快递订单'
        verbose_name_plural = "快递订单"
    # 代理人账号：ZZagent （固定）
    agent_account = models.CharField(max_length=200, default='ZZagent', verbose_name="代理人账号")
    # 发件人国家： (固定)
    sender_country = models.CharField(max_length=200, default='日本', verbose_name="发件人国家")
    # 发件人省： (固定)
    sender_province = models.CharField(max_length=200, default='埼玉县', verbose_name="发件人省")
    # 发件人市： (固定)
    sender_city = models.CharField(max_length=200, default='川口市', verbose_name="发件人市")
    # 发件人区（县）： (固定)
    sender_district = models.CharField(max_length=200, default='幸町', verbose_name="发件人区（县）")
    # 发件人地址： (固定)
    sender_address = models.CharField(max_length=200, default='〒 332-0016埼玉県川口市幸町1-14-10', verbose_name="发件人地址")
    # 散客名称：(自动)
    auto_recipient_name = models.CharField(max_length=200, verbose_name="散客名称", default='')

    #发件人姓名：选填    
    sender_name = models.CharField(max_length=200, null=True, verbose_name="发件人姓名(选填)", blank=True, default='')
    #发件登录日期时间 (自动)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="发件登录时间")
    #发件人微信名字：选填
    sender_wechat_name = models.CharField(max_length=200, null=True, verbose_name="发件人微信名字(选填)", blank=True, default='')
    #发件人微信号：（必须填写）
    sender_wechat_num = models.CharField(max_length=200, verbose_name="发件人微信号", default='')
    #发件人手机号码：选填
    mobile_regex = RegexValidator(regex=r'(^0[789]0[0-9]{4}[0-9]{4}$)|^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9]{3})[0-9]{8}$', message="请输入日本或中国手机号码(不加-)")
    sender_mobile_num = models.CharField(validators=[mobile_regex], max_length=17, verbose_name="发件人手机号码", default='')
    #发件店铺
    shop = models.CharField(max_length=200, null=True, verbose_name="发件店铺")

    
    # 收件人姓名：（必须填写）
    recipient_name = models.CharField(max_length=200, verbose_name="收件人姓名", default='')
    # 收件人手机号码: （必须填写）
    ch_phone_regex = RegexValidator(regex=r'^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9]{3})[0-9]{8}$', message="请输入中国手机号码")
    recipient_phone_num = models.CharField(max_length=200, validators=[ch_phone_regex], verbose_name="收件人手机号码", default='')
    # 收件人国家：（中国） 固定
    recipient_country = models.CharField(max_length=200, default='中国', verbose_name="收件人国家")
    # 收件人省：（可选择）
    recipient_province = models.CharField(max_length=200, verbose_name="收件人省", default='')
    # 收件人市：（可选择）
    recipient_city = models.CharField(max_length=200, verbose_name="收件人市", default='')
    # 收件人区（县）：（可选择）
    recipient_district = models.CharField(max_length=200, verbose_name="收件人区（县）", default='')
    # 收件人详细地址：xx省xx市xx区（县）xx号
    recipient_addr = models.CharField(max_length=200, verbose_name="收件人详细地址", default='')
    # 收件人身份证号码： 
    id_regex = RegexValidator(regex=r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', message="请输入正确的身份证号")
    recipient_id = models.CharField(validators=[id_regex], max_length=200, verbose_name="收件人身份证号码", default='')
    # 收件人身份证照片上传：建议上传 如遇海关抽查不能及时提交身份证照片出现任何问题我司概不负责
    recipient_photo = models.ImageField(verbose_name="收件人身份证照片上传", blank=True, upload_to=user_photo_path) 

    # 快递单号
    track_number = models.CharField(max_length=200, verbose_name="快递单号", null=True, blank=True)
    # 包裹状态
    packet_state = models.CharField(max_length=20, verbose_name="包裹状态", default='未发送', blank=True)

    def save(self, *args, **kwargs):
        if not self.sender_name:
            self.sender_name = '申通国际日本站'
        self.auto_recipient_name = self.recipient_name
        if self.track_number:
            self.packet_state = '已发送'
        if self.recipient_photo:
            try:
                self.recipient_photo = edit_photo_before_save(self.recipient_photo)
            except:
                pass
        super(Express, self).save(*args, **kwargs)


    def __str__(self):
        return self.sender_wechat_num + '-----' + str.split(str(self.created_date), '.')[0]+ '-----' + str(self.track_number)

