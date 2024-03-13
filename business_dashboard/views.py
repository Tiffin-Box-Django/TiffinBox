from django.shortcuts import render

from business_dashboard.forms import TiffinForm
from user_dashboard.models import Tiffin, TBUser


def index(request):
    return render(request, 'base.html', {})

def tiffin(request):
    return render(request, template_name='business_dashboard/tiffin_list.html', context={})

def add_tiffin(request):
    msg=''
    if request.method == 'POST':
        form = TiffinForm(request.POST)
        if form.is_valid():
            tiffin_item = form.save(commit=False)
            tiffin_item.save()
            msg='Tiffin added'
    else:
        form = TiffinForm()
    return render(request, 'business_dashboard/add_tiffin.html', context={'form': form, 'msg': msg})


def business_profile(request, username):
    user = TBUser.objects.get(username=username)
    return render(request, 'business_dashboard/profile.html', context={'user': user})