from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExpressForm, TrackForm


# def index_kawa(request):
#     return render(request, 'etrack/kawa/index.html')

# def ensure_kawa(request):
#     return render(request, 'etrack/kawa/ensure.html')

def index_ike(request):
    if request.method == 'POST':
        form1 = ExpressForm(request.POST)
        if form1.is_valid():
            return render(request, 'etrack/ike/index.html', {'path':'etrack:ensure_ike'})
    else: 
        form1 = ExpressForm()
        form2 = TrackForm()
    return render(request, 'etrack/ike/index.html', {'path':'etrack:ensure_ike', 'form1': form1, 'form2':form2})

def ensure_ike(request):
    return render(request, 'etrack/ike/ensure.html')
