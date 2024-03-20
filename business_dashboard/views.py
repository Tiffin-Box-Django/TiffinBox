from django.db.migrations import serializer
from django.shortcuts import render, redirect, get_object_or_404
from business_dashboard.forms import TiffinForm, SignUpForm, EditTiffinForm, EditProfileForm
from user_dashboard.models import Tiffin, TBUser, Order, OrderItem
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return redirect("business_dashboard:tiffin")
    else:
        return redirect("business_dashboard:login")

@login_required
def tiffin(request):
    return render(request, template_name='business_dashboard/tiffin.html', context={})
  
@login_required
def add_tiffin(request):
    if request.method == 'POST':
        form = AddTiffinForm(request.POST, request.FILES)
        if form.is_valid():
            business_user = request.user.id
            tiffin_item = form.save(commit=False)
            tiffin_item.business_id = TBUser.objects.get(pk=business_user)
            if 'image' in request.FILES:
                tiffin_item.image = request.FILES['image']
            tiffin_item.save()
            return redirect('business_dashboard:tiffin')
        return render(request, 'business_dashboard/add-tiffin.html', {'form': form})
    else:
        form = AddTiffinForm()
    return render(request, 'business_dashboard/add-tiffin.html', {'form': form})

# @login_required
def business_profile(request):
    user = get_object_or_404(TBUser, username=request.user.username, is_active=True)
    return render(request, 'business_dashboard/profile.html', context={'user': user})


def signup(request):
    if request.user.is_authenticated:
        return redirect("business_dashboard:index")

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
    if request.user.is_authenticated:
        return redirect("business_dashboard:index")

    if request.method == 'POST':
        msg = ''
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.client_type == 1:
                login(request, user)
                return redirect('business_dashboard:tiffin')
            else:
                msg = 'Invalid Username or Password!' #This message is being overridden by the error message from AuthenticationForm
                return render(request, 'business_dashboard/login.html', {'msg': msg})
    else:
        form = AuthenticationForm()
    return render(request, 'business_dashboard/login.html', {'form': form})

@login_required
def edit_tiffin(request, tiffin_id):
    the_tiffin = get_object_or_404(Tiffin, id=tiffin_id)
    if request.method == 'POST':
        form = EditTiffinForm(request.POST)
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

  
def edit_profile(request):
    user_profile = get_object_or_404(TBUser, username=request.user.username, is_active=True)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user_profile.profile_picture = form.cleaned_data['profile_picture']
            user_profile.username = form.cleaned_data['username']
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.email = form.cleaned_data['email']
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.shipping_address = form.cleaned_data['shipping_address']
            user_profile = form.save(commit=False)
            if 'image' in request.FILES:
                user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.save()
            return redirect("business_dashboard:profile")
    else:
        form = EditProfileForm(instance=user_profile)
    return render(request, "business_dashboard/edit-profile.html", {'user_profile': user_profile, 'form': form})

  
@login_required
def orders(request, order_status):
    # 0 1 2 3
    if order_status == 0:
        order_type = "Delivered"
        order_items = OrderItem.objects.filter(order_id__status=0).order_by("-order_id__created_date")
    elif order_status == 1:
        order_type = "Order Placed"
        order_items = OrderItem.objects.filter(order_id__status=1).order_by("-order_id__created_date")
    elif order_status == 2:
        order_type = "Shipped"
        order_items = OrderItem.objects.filter(order_id__status=2).order_by("-order_id__created_date")
    elif order_status == 3:
        order_type = "Cancelled"
        order_items = OrderItem.objects.filter(order_id__status=3).order_by("-order_id__created_date")
    else:
        order_type = "All"
        order_items = OrderItem.objects.all().order_by("-order_id__created_date")

    updated_orders = []

    for order in order_items:
        updated_orders.append((dict(order.order_id.ORDER_STATUS)[order.order_id.status], dict(order.order_id.PAYMENT_TYPES)[order.order_id.payment_method], order))

    return render(request, "business_dashboard/orders.html", {"order_type": order_type, "orders": updated_orders})


@login_required
def update_order_status(request, order_id):
    if request.method == "POST":
        the_order = OrderItem.objects.get(id=order_id)
        order_item = Order.objects.get(id=the_order.order_id.id)

        order_item.status = int(request.POST['order_status_change'])
        order_item.save()
        return redirect("business_dashboard:orders", int(request.POST['order_status_change']))
    else:
        return redirect("business_dashboard:orders", 0)

