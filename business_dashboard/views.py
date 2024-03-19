from django.shortcuts import render, redirect, get_object_or_404
from business_dashboard.forms import TiffinForm, SignUpForm, EditTiffinForm
from user_dashboard.models import Tiffin, TBUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    return redirect("business_dashboard:login")

@login_required
def tiffin(request):
    return render(request, template_name='business_dashboard/tiffin.html', context={})
  
@login_required
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
        # we have request.FILES for image files upload
        form = SignUpForm(request.POST, request.FILES)

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

def businessLoginPage(request):
    if request.method == 'POST':
        # form = LoginForm(request.POST)
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return render(request, 'business_dashboard/tiffin.html')
            else:
                messages.error(request, 'Username or Password is incorrect!')
    else:
        form = AuthenticationForm()
    return render(request, 'business_dashboard/login.html', {'form': form})

@login_required
def edit_tiffin(request, tiffin_id):
    the_tiffin = get_object_or_404(Tiffin, id=tiffin_id)
    if request.method == 'POST':
        form = TiffinForm(request.POST)
        if form.is_valid():
            the_tiffin.tiffin_name = form.cleaned_data['tiffin_name']
            the_tiffin.tiffin_description = form.cleaned_data['tiffin_description']
            the_tiffin.meal_type = form.cleaned_data['meal_type']
            the_tiffin.calories = form.cleaned_data['calories']
            the_tiffin.price = form.cleaned_data['price']
            the_tiffin.free_delivery_eligible = form.cleaned_data['free_delivery_eligible']
            the_tiffin.save()
            return redirect("business_dashboard:index")

        return render(request, 'business_dashboard/edit-tiffin.html', {"tiffin_id": tiffin_id, 'form': form})
    else:
        form = EditTiffinForm(instance=the_tiffin, initial={'schedule_id': the_tiffin.schedule_id})

    return render(request, "business_dashboard/edit-tiffin.html", {"tiffin_id": tiffin_id, 'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("business_dashboard:login")
