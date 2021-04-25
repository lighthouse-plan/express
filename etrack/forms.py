from django import forms
from django.forms import ModelForm
from .models import Express
from django.core.validators import RegexValidator
from django.forms import Field


class ExpressForm(ModelForm):
    class Meta:
        model = Express
        fields = ['sender_name', 'sender_mobile_num', 'sender_wechat_name', 'sender_wechat_num', 'shop','recipient_name', 'recipient_phone_num', 'recipient_country', 'recipient_province', 'recipient_city', 'recipient_district', 'recipient_addr', 'recipient_id',  'recipient_photo']
    def __init__(self, *args, **kwargs):
        super(ExpressForm, self).__init__(*args, **kwargs)
        print(self.fields.keys())
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = "这一栏是必填项。"
        
    
class TrackForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TrackForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = "这一栏是必填项。"
    ch_phone_regex = RegexValidator(regex=r'^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9]{3})[0-9]{8}$', message="请输入中国手机号码")
    recipient_phone_num = forms.CharField(max_length=200, validators=[ch_phone_regex], label="收件人手机号码")