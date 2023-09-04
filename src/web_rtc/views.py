from django.shortcuts import render

# Create your views here.


def web_rtc(request):
    context = {
        'title': 'web_rtc',
    }
    return render(request, 'web_rtc/web_rtc.html',  context=context)
