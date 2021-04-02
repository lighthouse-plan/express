from django import forms
from django.forms import ModelForm
from .models import Express
from django.core.validators import RegexValidator

class ExpressForm(ModelForm):
    class Meta:
        model = Express
        exclude = ['created_date', 'track_number', 'packet_state']
    
    

class TrackForm(forms.Form):
    ch_phone_regex = RegexValidator(regex=r'^(13[0-9]|14[01456879]|15[0-3,5-9]|16[2567]|17[0-8]|18[0-9]|19[0-3,5-9]{3})[0-9]{8}$', message="请输入中国手机号码")
    recipient_phone_num = forms.CharField(max_length=200, validators=[ch_phone_regex], label="收件人手机号码")