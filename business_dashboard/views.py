from django.shortcuts import render, redirect
from business_dashboard.forms import TiffinForm, SignUpForm
from user_dashboard.models import Tiffin, TBUser


def index(request):
    return render(request, 'base.html', {})


def tiffin(request):
    return render(request, template_name='business_dashboard/tiffin_list.html', context={})


def add_tiffin(request):
    msg = ''
    if request.method == 'POST':
        form = TiffinForm(request.POST)
        if form.is_valid():
            tiffin_item = form.save(commit=False)
            tiffin_item.save()
            msg = 'Tiffin added'
    else:
        form = TiffinForm()
    return render(request, 'business_dashboard/add_tiffin.html', context={'form': form, 'msg': msg})


def business_profile(request, username):
    user = TBUser.objects.get(username=username)
    return render(request, 'business_dashboard/profile.html', context={'user': user})


def signup(request):
    special_characters = '"!@#$%^&*()-+?=,<>/"'
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        #verify the username
        username = request.POST['username']
        if any(char in special_characters for char in username):
            form.add_error('username', 'Username cannot contain special characters')
            return render(request, 'business_dashboard/sign-up.html', {'form': form})

        if form.is_valid():
            # validate the form data by not commiting into db
            user = form.save()
            user.set_password(form.cleaned_data.get('password1'))
            user.client_type = 1
            # save into db
            user.save()

            return redirect('business_dashboard:login')
    else:
        form = SignUpForm()
    return render(request, "business_dashboard/sign-up.html", {'form': form})
