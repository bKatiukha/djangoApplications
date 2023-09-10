from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def web_rtc(request):
    context = {
        'title': 'web_rtc',
    }
    return render(request, 'web_rtc/web_rtc.html',  context=context)
