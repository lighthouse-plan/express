from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ExpressForm, TrackForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Express
from django.http import Http404
from django.urls import reverse
from datetime import datetime


def get_shop_name(shop):
    if shop == 'ikebukuro':
        return '池袋'
    if shop == 'kawaguchi':
        return '川口'
    else:
        raise Http404(f"{shop} does not exist")

def index(request, shop):
    try:
        shop_name = get_shop_name(shop)
    except:
        raise Http404(f"{shop} does not exist")
    if request.method == 'POST':
        form1 = ExpressForm(request.POST, request.FILES)
        request.session['form_data'] = request.POST
            
        if form1.is_valid():
            form1.save()
            email_from = settings.EMAIL_HOST_USER
            send_mail(
                'Subject here',
                'Here is the message.',
                email_from,
                ['1173359575zmn@gmail.com'],
                fail_silently=False,
            )
            ts = str(datetime.timestamp(datetime.now()))
            return HttpResponseRedirect(reverse('etrack:confirm', args=(shop, ts)))
    if 'form_data' in request.session:
        form1 = ExpressForm(request.session['form_data'])
    else: 
        form1 = ExpressForm()
    form2 = TrackForm()
    return render(request, 'etrack/index.html', {'shop':shop, 'shop_name':shop_name, 'form1': form1, 'form2': form2})

def confirm(request, shop, ts):
    try:
        shop_name = get_shop_name(shop)
    except:
        raise Http404(f"{shop} does not exist")
    return render(request, 'etrack/confirm.html', {'shop':shop, 'shop_name':shop_name})
def search(request, shop):
    try:
        shop_name = get_shop_name(shop)
    except:
        raise Http404(f"{shop} does not exist")
    has_result = False
    result = []
    error_message = ''
    if request.method == 'POST':
        has_result = True
        form2 = TrackForm(request.POST)
        if form2.is_valid():
            recipient_phone_num = form2.cleaned_data['recipient_phone_num']
            expresses = Express.objects.filter(recipient_phone_num=recipient_phone_num)
            for e in expresses:
                pair = {}
                pair['datetime'] = e.created_date.strftime("%Y-%m-%d, %H:%M:%S")
                if e.track_number is None:
                    pair['state'] = e.packet_state
                else:
                    pair['state'] = e.track_number
                result.append(pair)
        else:
            error_message = '请输入收件人中国手机号码'
    form1 = ExpressForm()
    form2 = TrackForm()
    return render(request, 'etrack/index.html', {'shop':shop, 'shop_name':shop_name, 'form1': form1, 'form2': form2, 'has_result':has_result, 'result':result, 'error_message':error_message})

