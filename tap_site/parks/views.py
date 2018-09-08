from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Review, Parks, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

@cache_page(10 * 1)
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/parks/review_list.html', context)

@cache_page(10 * 1)
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/parks/review_detail.html', {'review': review})


def parks_list(request):
    parks_list = Parks.objects.order_by('-name')
    context = {'parks_list':parks_list}
    return render(request, 'reviews/parks/parks_list.html', context)

@cache_page(10 * 1)
def parks_detail(request, parks_id):
    parks = get_object_or_404(Parks, pk=parks_id)
    form = ReviewForm()
    return render(request, 'reviews/parks/parks_detail.html', {'parks': parks,'form': form})

@login_required
def add_review(request, parks_id):
    if request.method == "POST":
        parks = get_object_or_404(Parks, pk=parks_id)
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            image = form.cleaned_data['image']
            user_name = request.user.username
            review = Review()
            review.parks = parks
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
            return HttpResponseRedirect(reverse('parks:parks_detail', args=(parks.id,)))
    else:
        form = ReviewForm()

    return render(request, 'reviews/parks/parks_detail.html', {'form': form})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)

@login_required
def user_recommendation_list(request):
    
    # get request user reviewed offices
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('parks')
    user_reviews_parks_ids = set(map(lambda x: x.parks.id, user_reviews))

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
            .exclude(parks__id__in=user_reviews_parks_ids)
    other_users_reviews_parks_ids = set(map(lambda x: x.parks.id, other_users_reviews))
    
    # then get a offices list including the previous IDs, order by rating
    parks_list = sorted(
        list(Parks.objects.filter(id__in=other_users_reviews_parks_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'parks_list': parks_list}
    )

# Create your views here.
