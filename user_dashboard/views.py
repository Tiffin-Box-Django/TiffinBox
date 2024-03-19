from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Tiffin, Testimonial, TBUser, Review
from .forms import ExploreSearchForm, FilterForm, SignUpForm
from django.contrib.auth import views as auth_views

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
            # Custom validation logic
            cleaned_data = form.cleaned_data

            # Check if username contains any special characters
            username = cleaned_data.get('username')
            if any(char.isdigit() or not char.isalnum() for char in username):
                form.add_error('username', 'Username must contain only alphanumeric characters.')
                return render(request, 'registration/signup.html', {'form': form})

            # Save the user
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('/user/login')  # Redirect to login page after successful signup
        else:
            return render(request, 'registration/signup.html', {'form': form, 'error': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class UserLogin(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return self.request.GET.get('next', '/user/explore')

def cart(request):
    #tiffins = Tiffin.objects.filter(id = 1)  # Query all Tiffin objects for demonstration
    tiffins = Tiffin.objects.all()  # Query all Tiffin objects for demonstration
    totalPrice = 0
    for tiffin in tiffins:
        totalPrice = tiffin.price + totalPrice
    return render(request, 'user_dashboard/cart.html', {'tiffins': tiffins, 'totalPrice': totalPrice})

def deleteCartItem(request,id):
    dele = Tiffin.objects.get(id=id)
    dele.delete()
    return redirect('user_dashboard:cart')

def user_profile(request, username):
    user = TBUser.objects.get(username=username)
    return render(request, 'business_dashboard/profile.html', context={'user': user})

def logout(request):
    ref = request.GET.get('next', '/user')
    auth_views.auth_logout(request)
    return redirect(ref)
