from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Review, Hotels, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


@cache_page(10 * 1)
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/hotels/review_list.html', context)

@cache_page(10 * 1)
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/hotels/review_detail.html', {'review': review})


def hotels_list(request):
    hotels_list = Hotels.objects.order_by('-name')
    context = {'hotels_list':hotels_list}
    return render(request, 'reviews/hotels/hotels_list.html', context)

@cache_page(10 * 1)
def hotels_detail(request, hotels_id):
    hotels = get_object_or_404(Hotels, pk=hotels_id)
    form = ReviewForm()
    return render(request, 'reviews/hotels/hotels_detail.html', {'hotels': hotels,'form': form})

@login_required
def add_review(request, hotels_id):
    if request.method == "POST":
        hotels = get_object_or_404(Hotels, pk=hotels_id)
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            image = form.cleaned_data['image']
            user_name = request.user.username
            review = Review()
            review.hotels = hotels
            review.user_name = user_name
            review.rating = rating
            review.comment = comment
            review.image = image
            review.pub_date = datetime.datetime.now()
            review.save()
            update_clusters()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('hotels:hotels_detail', args=(hotels.id,)))
    else:
        form = ReviewForm()

    return render(request, 'reviews/hotels/hotels_detail.html', {'form': form})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    
    # get request user reviewed offices
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('hotels')
    user_reviews_hotels_ids = set(map(lambda x: x.hotels.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    
    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding offices reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(hotels__id__in=user_reviews_hotels_ids)
    other_users_reviews_hotels_ids = set(map(lambda x: x.hotels.id, other_users_reviews))
    
    # then get a offices list including the previous IDs, order by rating
    hotels_list = sorted(
        list(Hotels.objects.filter(id__in=other_users_reviews_hotels_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'hotels_list': hotels_list}
    )

# Create your views here.
