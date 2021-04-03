from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExpressForm, TrackForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Express


# def index_kawa(request):
#     return render(request, 'etrack/kawa/index.html')

# def ensure_kawa(request):
#     return render(request, 'etrack/kawa/ensure.html')

def index_ike(request):
    if request.method == 'POST':
        form1 = ExpressForm(request.POST)
        form2 = TrackForm()
        if form1.is_valid():
            print(form1.cleaned_data)
            form1.save()
            email_from = settings.EMAIL_HOST_USER
            send_mail(
                'Subject here',
                'Here is the message.',
                email_from,
                ['1173359575zmn@gmail.com'],
                fail_silently=False,
            )
            return render(request, 'etrack/ike/index.html', {'path':'etrack:search_ike', 'form1': form1, 'form2': form2})
    else: 
        form1 = ExpressForm()
        form2 = TrackForm()
    return render(request, 'etrack/ike/index.html', {'path':'etrack:search_ike', 'form1': form1, 'form2': form2})

def search_ike(request):
    form1 = ExpressForm()
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
            error_message = '请输入收件人手机号码'
    return render(request, 'etrack/ike/index.html', {'path':'etrack:search_ike', 'form1': form1, 'form2': form2, 'has_result':has_result, 'result':result, 'error_message':error_message})
