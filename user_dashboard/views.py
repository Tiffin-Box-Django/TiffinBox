from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.detail import DetailView
from TiffinBox.settings import EMAIL_HOST_USER

from .forms import ExploreSearchForm, FilterForm, SignUpForm, EditProfileForm
from .models import Tiffin, Testimonial, TBUser, Review, Order, OrderItem
from .tokens import account_activation_token


def explore(request):
    if request.method == 'POST':
        post_data = request.POST.dict()
        if post_data.get("avg_rating"):
            post_data["avg_rating"] = float(post_data["avg_rating"])

        if post_data.get("calories"):
            calories = [int(c.strip()) for c in post_data["calories"].split("-")]
            post_data["calories__gte"] = float(calories[0])
            post_data["calories__lte"] = float(calories[1])
            post_data.pop("calories")

        if post_data.get("price"):
            prices = [int(c.strip().replace("$", "")) for c in post_data["price"].split("-")]
            post_data["price__gte"] = float(prices[0])
            post_data["price__lte"] = float(prices[1])
            post_data.pop("price")

        if post_data.get('free_delivery_eligible'):
            if "on" in post_data['free_delivery_eligible']:
                post_data['free_delivery_eligible'] = True
            else:
                post_data['free_delivery_eligible'] = False

        post_data.pop("csrfmiddlewaretoken")
        tiffins = Tiffin.objects.filter(
            **{k: v for k, v in post_data.items() if v != '' and v is not None})
    else:
        if request.GET.get('search'):
            tiffins = Tiffin.objects.filter(tiffin_name__contains=request.GET['search'])
        else:
            tiffins = Tiffin.objects.all()

    formatted_tiffins = []
    for tiffin in tiffins:
        formatted_tiffins.append({"id": tiffin.id, "name": tiffin.tiffin_name, "photo": tiffin.image,
                                  "business": tiffin.business_id.first_name + tiffin.business_id.last_name,
                                  "category": tiffin.meal_name(),
                                  "rating": list(range(int(round(tiffin.avg_rating)))),
                                  "price": tiffin.price})
    search_form = ExploreSearchForm(request.GET) if request.GET else ExploreSearchForm()
    filters_form = FilterForm(initial=request.POST)

    return render(request, 'user_dashboard/explore.html',
                  {'searchForm': search_form, 'filtersForm': filters_form,
                   'tiffins': formatted_tiffins, "filter_params": {}})


class TiffinDetails(DetailView):
    model = Tiffin
    template_name = 'user_dashboard/tiffindetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tiffin_id = self.kwargs["pk"]
        recently_viewed = self.request.session.get("recently_viewed", [])
        if recently_viewed:
            if tiffin_id in recently_viewed:
                recently_viewed.remove(tiffin_id)
            recently_viewed.insert(0, tiffin_id)
            self.request.session["recently_viewed"] = recently_viewed
        else:
            self.request.session["recently_viewed"] = [tiffin_id]

        context["recently_viewed"] = self.request.session["recently_viewed"]

        context["review_counts"] = Review.objects.filter(tiffin_id=tiffin_id).count()
        reviews = Review.objects.filter(tiffin_id=tiffin_id).values("user__first_name", "user__last_name",
                                                                    "comment", "rating", "created_date",
                                                                    "user__profile_picture")
        reviews_grid, tmp = [], []
        for idx, review in enumerate(reviews):
            if review["user__profile_picture"].startswith("image"):
                review["user__profile_picture"] = f"http://{self.request.get_host()}/{review['user__profile_picture']}"

            if idx % 3 != 0 or idx == 0:
                tmp.append(review)
            else:
                reviews_grid.append(tmp)
                tmp = [review]
        if tmp:
            reviews_grid.append(tmp)
        context["reviews_grid"] = reviews_grid

        tiffin_extras = [("Delivery Frequency", kwargs["object"].schedule_id.enum(), "calendar-week"),
                         ("Meal Plan", dict(kwargs["object"].MEAL)[kwargs["object"].meal_type], "basket"),
                         ("Calories", kwargs["object"].calories, "lightning")]

        context["tiffin_extras"] = tiffin_extras
        recommended = Tiffin.objects.exclude(id=tiffin_id).filter(business_id__id=kwargs["object"].business_id.id)[:4]
        context["recommended_tiffins"] = recommended
        context["is_authenticated"] = self.request.user.is_authenticated
        if self.request.GET.get("disallow") == "true":
            context["disallow"] = True
        else:
            context["disallow"] = False
        # messages.success(self.request, "Item(s) added to cart!")
        return context


def business_details(request, pk):
    business = get_object_or_404(TBUser, pk=pk)

    if business.client_type != 1:
        pass

    tiffins = Tiffin.objects.filter(business_id=business.pk)

    if request.method == 'POST':
        # filters_form = FilterForm(request.POST)
        post_data = request.POST.dict()
        if post_data.get('meal_type'):
            tiffins = tiffins.filter(meal_type=post_data['meal_type'])

        if post_data.get("avg_rating"):
            post_data["avg_rating"] = float(post_data["avg_rating"])

        if post_data.get("calories"):
            calories = [int(c.strip()) for c in post_data["calories"].split("-")]
            post_data["calories__gte"] = float(calories[0])
            post_data["calories__lte"] = float(calories[1])
            post_data.pop("calories")

        if post_data.get("price"):
            prices = [int(c.strip().replace("$", "")) for c in post_data["price"].split("-")]
            post_data["price__gte"] = float(prices[0])
            post_data["price__lte"] = float(prices[1])
            post_data.pop("price")

        if post_data.get('free_delivery_eligible'):
            if post_data['free_delivery_eligible'] == "on":
                post_data['free_delivery_eligible'] = True
            else:
                post_data['free_delivery_eligible'] = False

        post_data.pop("csrfmiddlewaretoken")
        tiffins = tiffins.filter(
            **{k: v for k, v in post_data.items() if v != '' and v is not None})

        filters_form = FilterForm(initial=request.POST)

    else:
        filters_form = FilterForm()

    ph_no = business.phone_number
    ph_no = ph_no[0:3] + "-" + ph_no[3:6] + "-" + ph_no[6:10]
    business.phone_number = ph_no

    context = {
        'business': business,
        'tiffins': tiffins,
        'is_authenticated': request.user.is_authenticated,
        'filtersForm': filters_form,
    }

    return render(request, 'user_dashboard/businessdetails.html', context)


@login_required
def update_cart(request):
    response = HttpResponse(status=204)
    if request.method != "GET":
        return response

    tiffin_id = request.GET["tiffin_id"]
    quantity = int(request.GET["quantity"])

    tiffin = Tiffin.objects.get(id=tiffin_id)
    try:
        user_order = Order.objects.get(user_id=TBUser.objects.get(id=request.user.id), status=4)
    except Order.DoesNotExist:
        user_order = Order(user_id=TBUser.objects.get(id=request.user.id), total_price=0)
        user_order.save()

    user_order.total_price += Decimal(tiffin.price * quantity)
    user_order.save()

    try:
        order_item = OrderItem.objects.get(order_id=Order.objects.get(id=user_order.id), tiffin_id=tiffin)
        order_item.quantity += quantity
        order_item.save()
    except OrderItem.DoesNotExist:
        order_item = OrderItem(order_id=user_order, tiffin_id=tiffin, quantity=quantity)
        order_item.save()
    return response


@login_required
def add_review(request, tiffinid: int):
    if request.method != "POST":
        return HttpResponse(status=204)

    if request.session.get("reviewed_tiffins"):
        if tiffinid in request.session["reviewed_tiffins"]:
            return redirect(reverse("user_dashboard:tiffindetails", kwargs={"pk": 3}) + "?disallow=true")
        else:
            request.session["reviewed_tiffins"].append(tiffinid)
    else:
        request.session["reviewed_tiffins"] = [tiffinid]

    tmp = Review(user=TBUser.objects.get(id=request.user.id), comment=request.POST["review-text"],
                 rating=int(request.POST["review-stars"]), tiffin=Tiffin.objects.get(id=tiffinid))
    tmp.save()

    tmp = Tiffin.objects.get(id=tiffinid)
    tmp.avg_rating = Decimal(Review.objects.filter(tiffin=tmp).aggregate(Avg('rating'))["rating__avg"])
    tmp.save()

    return redirect("user_dashboard:tiffindetails", pk=tiffinid)


def landing(request):
    username = None
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = TBUser.objects.get(pk=user_id)
        username = user.username

    if request.GET.get('search'):
        form = ExploreSearchForm(request.GET)
        if form.is_valid():
            response = HttpResponseRedirect(
                reverse('user_dashboard:explore') + '?search=' + form.cleaned_data['search'])
            response.set_cookie('last_search', form.cleaned_data['search'])
            return response
    else:
        form = ExploreSearchForm()

    # Proceed with rendering the landing page
    top_tiffins = Tiffin.objects.annotate(rating=Avg('avg_rating')).order_by('-rating')[:4]
    top_businesses = TBUser.objects.annotate(avg_rating=Avg('tiffin__review__rating')).filter(
        client_type=1).order_by('-avg_rating')[:4]
    testimonials = Testimonial.objects.all()

    return render(request, 'user_dashboard/landing.html', {
        'testimonials': testimonials,
        'top_tiffins': top_tiffins,
        'top_businesses': top_businesses,
        'search_form': form,
        'username': username  # Pass the username to the template context
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password1'])
            user.save()
            activateEmail(request, user)
            messages.success(request, 'Please check your email to confirm your registration.')
            # Redirect to login page after successful signup
            return redirect('user_dashboard:login')
        else:

            return render(request, 'user_dashboard/signup.html',
                          {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'user_dashboard/signup.html', {'form': form})


def activateEmail(request, user):
    mail_subject = 'Activate Your TiffinBox Account Now!'
    message = render_to_string("user_dashboard/account_activation_email.html",
                               {'user': user.first_name, 'domain': get_current_site(request).domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user),
                                'protocol': 'https' if request.is_secure() else 'http'})
    send_mail(mail_subject, message, EMAIL_HOST_USER, [user.email])


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # messages.success(request, "Thank you for your email confirmation. Please login your account.")
        messages.success(request,
                         "Cheers! Your email verification is a success. Please Login & start ordering your favorite Tiffins now!")
        return redirect('user_dashboard:login')
    else:
        messages.error(request, "Unfortunately, the activation link has expired.")
    return redirect('user_dashboard:landing')


class UserLogin(LoginView):
    template_name = 'user_dashboard/login.html'

    def get_initial(self):
        return {"username": self.request.COOKIES['uname']} if self.request.COOKIES.get('uname') else {}

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        try:
            user = TBUser.objects.get(username=username)
            if user.client_type == 1:
                messages.error(self.request, "Business owners, Please login here.")
                return redirect('business_dashboard:login')
        except TBUser.DoesNotExist:
            pass
        # Set session data upon successful login
        user = form.get_user()
        self.request.session['user_id'] = user.id
        self.request.session['username'] = user.username
        self.request.session.modified = True

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ufname"] = self.request.COOKIES.get("ufname")
        return context

    def get_success_url(self):
        return self.request.GET.get('next', '/')


def cart(request):
    tiffins = OrderItem.objects.filter(order_id__user_id__id=request.user.id, order_id__status=4)
    totalPrice = 0
    for tiffin in tiffins:
        totalPrice = (tiffin.quantity * tiffin.tiffin_id.price) + totalPrice
    return render(request, 'user_dashboard/cart.html', {'tiffins': tiffins, 'totalPrice': totalPrice})


def deleteCartItem(request, id):
    order_item = OrderItem.objects.get(id=id)
    order_id = order_item.order_id

    order_items_count = OrderItem.objects.filter(order_id=order_id).count()
    order_item_price = order_item.quantity * order_item.tiffin_id.price

    order_item.delete()
    order_obj = Order.objects.get(id=order_id.id)
    if order_items_count == 1:
        order_obj.delete()
    else:
        order_obj.total_price -= order_item_price
        order_obj.save()

    return redirect('user_dashboard:cart')


def placeOrder(request):
    user = TBUser.objects.get(id=request.user.id)
    order = Order.objects.get(user_id__id=request.user.id, status=4)
    if request.user.is_authenticated:
        if request.method == 'POST':
            shipping_address = request.POST.get('shippingAddress')
            phone_number = request.POST.get('phoneNumber')

            if not shipping_address:
                shipping_address = user.shipping_address
            elif not phone_number:
                phone_number = user.phone_number
        else:
            phone_number = user.phone_number
            shipping_address = user.shipping_address

        order.shipping_address = shipping_address
        order.phone_number = phone_number
        order.status = 1
        order.save()

    return render(request, 'user_dashboard/placeOrder.html')


def order_history(request):
    orderItems = OrderItem.objects.filter(order_id__user_id__id=request.user.id).exclude(order_id__status=4)
    orderHistory = Order.objects.filter(user_id__id=request.user.id).exclude(status=4).order_by('-created_date')
    for order in orderHistory:
        order.orderitem_set.set(orderItems.filter(order_id=order.id))

    return render(request, 'user_dashboard/orderHistory.html', {'orderHistory': orderHistory})


def user_profile(request):
    user = get_object_or_404(TBUser, username=request.user.username, is_active=True)
    return render(request, 'user_dashboard/profile.html', context={'user': user})


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
            return redirect("user_dashboard:profile")
    else:
        form = EditProfileForm(instance=user_profile)

    return render(request, "user_dashboard/edit-profile.html", {'user_profile': user_profile, 'form': form})


def logout(request):
    ref = request.GET.get('next', '/login/')
    auth_views.auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(ref)
