from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Tiffin, Testimonial, TBUser, Review, Order, OrderItem
from .forms import ExploreSearchForm, FilterForm, SignUpForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import send_mail


def explore(request):
    if request.method == 'POST':
        post_data = request.POST.dict()
        if post_data.get("avg_rating"):
            post_data["avg_rating"] = float(post_data["avg_rating"])

        if post_data.get("calories"):
            calories = [int(c.strip()) for c in post_data["calories"].split("-")]
            post_data["calories__gt"] = float(calories[0])
            post_data["calories__lt"] = float(calories[1])
            post_data.pop("calories")

        if post_data.get("price"):
            prices = [int(c.strip().replace("$", "")) for c in post_data["price"].split("-")]
            post_data["price__gt"] = float(prices[0])
            post_data["price__lt"] = float(prices[1])
            post_data.pop("price")

        if post_data.get('free_delivery_eligible'):
            if post_data['free_delivery_eligible'] == "on":
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
                                  "rating": list(range(int(round(tiffin.avg_rating)))),
                                  "price": tiffin.price})
    search_form = ExploreSearchForm()
    filters_form = FilterForm(initial={"free_delivery_eligible": False})

    return render(request, 'user_dashboard/explore.html',
                  {'searchForm': search_form, 'filtersForm': filters_form,
                   'tiffins': formatted_tiffins, "filter_params": {}})


class TiffinDetails(DetailView):
    model = Tiffin
    template_name = 'user_dashboard/tiffindetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_counts"] = Review.objects.filter(tiffin_id=self.kwargs["pk"]).count()
        reviews = Review.objects.filter(tiffin_id=self.kwargs["pk"]).values("user__first_name", "user__last_name",
                                                                            "comment", "rating", "created_date")
        reviews_grid, tmp = [], []
        for idx, review in enumerate(reviews):
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
        recommended = Tiffin.objects.exclude(id=self.kwargs["pk"]) \
                          .filter(business_id__id=kwargs["object"].business_id.id)[:4]
        context["recommended_tiffins"] = recommended
        context["is_authenticated"] = self.request.user.is_authenticated
        return context


def addcart(request, tiffin_id):
    return None


def landing(request):
    top_tiffins = Tiffin.objects.annotate(rating=Avg('avg_rating')).order_by('-rating')[:5]
    top_businesses = TBUser.objects.annotate(avg_rating=Avg('tiffin__review__rating')).filter(client_type=1).order_by(
        '-avg_rating')[:3]
    testimonials = Testimonial.objects.all()
    return render(request, 'user_dashboard/landing.html',
                  {'testimonials': testimonials, 'top_tiffins': top_tiffins, 'top_businesses': top_businesses})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.is_active=False
            user.set_password(form.cleaned_data['password1'])
            user.save()
            activateEmail(request, user)
            messages.success(request, 'Please check your email to confirm your registration.')
            # Redirect to login page after successful signup
            return redirect('user_dashboard:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return render(request, 'user_dashboard/signup.html', {'form': form, 'error': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'user_dashboard/signup.html', {'form': form})


def activateEmail(request, user):
    mail_subject = 'Activate Your TiffinBox Account Now!'
    message = render_to_string("user_dashboard/account_activation_email.html", {'user': user.first_name, 'domain': get_current_site(request).domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user), 'protocol': 'https' if request.is_secure() else 'http'})
    send_mail(mail_subject, message, 'raholsarvy@gmail.com', [user.email])

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
        messages.success(request, "Cheers! Your email verification is a success. Please Login & start ordering your favorite Tiffins now!")
        return redirect('user_dashboard:login')
    else:
        messages.error(request, "Unfortunately, the activation link has expired.")
    return redirect('user_dashboard:landing')


class UserLogin(LoginView):
    template_name = 'user_dashboard/login.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/')


def cart(request):
    #tiffins = Tiffin.objects.filter(id = 1)  # Query all Tiffin objects for demonstration
    #tiffins = OrderItem.objects.filter(order_id__status= 4, order_id__user_id= request.user.id)  # Query all Tiffin objects for demonstration
    tiffins = OrderItem.objects.filter(order_id__status= 4 )
    totalPrice = 0
    for tiffin in tiffins:
        totalPrice = tiffin.tiffin_id.price + totalPrice
    return render(request, 'user_dashboard/cart.html', {'tiffins': tiffins, 'totalPrice': totalPrice})

def deleteCartItem(request,id):
    dele = OrderItem.objects.get(id=id)
    dele.delete()
    return redirect('user_dashboard:cart')

def placeOrder(request):
    #tiffins = OrderItem.objects.filter(order_id__status=4,order_id__user_id=request.user.id)  # Query all Tiffin objects for demonstration
    tiffins = Order.objects.filter(status=4)  # Query all Tiffin objects for demonstration

    for order in tiffins:
        order.status = 1
        order.save()
    return render(request, 'user_dashboard/placeOrder.html')

def OrderHistory(request):
  orderHistory = Order.objects.filter(user_id = request.user.id)


def user_profile(request, username):
    user = TBUser.objects.get(username=username)
    return render(request, 'business_dashboard/profile.html', context={'user': user})

def logout(request):
    ref = request.GET.get('next', '/')
    auth_views.auth_logout(request)
    return redirect(ref)
