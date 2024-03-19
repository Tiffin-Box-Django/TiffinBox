from django.shortcuts import render, redirect, get_object_or_404
from business_dashboard.forms import TiffinForm, SignUpForm, EditTiffinForm, ForgotPassword
from user_dashboard.models import Tiffin, TBUser, Order, OrderItem, ResetPassword
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import uuid


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


def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(TBUser, email=email)
            if user.client_type == 1:
                code = uuid.uuid4()
                code_object = ResetPassword.objects.create(code=code)
                code_object.save()
                print(f"http://localhost:8000/business/reset-password/{code}")
            else:
                print("user not business")
    else:
        form = ForgotPassword()
    return render(request, "business_dashboard/forgot-password.html", {"form": form})


def reset_password(request, code):
    code
    return render(request, "business_dashboard/reset-password.html", {"code": code})