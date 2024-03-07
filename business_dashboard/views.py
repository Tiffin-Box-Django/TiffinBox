from django.shortcuts import render


def index(request):
    return render(request, 'base.html', {})

def tiffin(request):
    return render(request, template_name='business_dashboard/tiffin_list.html', context={})