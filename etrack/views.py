from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExpressForm, TrackForm
from django.core.mail import send_mail
from django.conf import settings


# def index_kawa(request):
#     return render(request, 'etrack/kawa/index.html')

# def ensure_kawa(request):
#     return render(request, 'etrack/kawa/ensure.html')

def index_ike(request):
    if request.method == 'POST':
        form1 = ExpressForm(request.POST)
        
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
            return render(request, 'etrack/ike/index.html', {'path':'etrack:ensure_ike', 'form1': form1, })
        else:
            print("tttttttttt")
    else: 
        form1 = ExpressForm()
        form2 = TrackForm()
    return render(request, 'etrack/ike/index.html', {'path':'etrack:ensure_ike', 'form1': form1, })

def ensure_ike(request):
    return render(request, 'etrack/ike/ensure.html')
