from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Review, Public_Office, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.views.decorators.cache import cache_page
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView



@cache_page(10 * 1)
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:99]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)

@cache_page(10 * 1)
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def public_office_list(request):
    public_office_list = Public_Office.objects.order_by('-name')
    context = {'public_office_list':public_office_list}
    return render(request, 'reviews/public_office_list.html', context)

@cache_page(10 * 1)
def public_office_detail(request, public_office_id):
    public_office = get_object_or_404(Public_Office, pk=public_office_id)
    form = ReviewForm()
    return render(request, 'reviews/public_office_detail.html', {'public_office': public_office,'form': form})

@login_required
def add_review(request, public_office_id):
    if request.method == "POST":
        public_office = get_object_or_404(Public_Office, pk=public_office_id)
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            image = form.cleaned_data['image']
            user_name = request.user.username
            review = Review()
            review.public_office = public_office
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
            return HttpResponseRedirect(reverse('reviews:public_office_detail', args=(public_office.id,)))
    else:
        form = ReviewForm()

    return render(request, 'reviews/public_office_detail.html', {'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)

@login_required
def user_recommendation_list(request):
    
    # get request user reviewed offices
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('public_office')
    user_reviews_public_office_ids = set(map(lambda x: x.public_office.id, user_reviews))

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
            .exclude(public_office__id__in=user_reviews_public_office_ids)
    other_users_reviews_public_office_ids = set(map(lambda x: x.public_office.id, other_users_reviews))
    
    # then get a offices list including the previous IDs, order by rating
    public_office_list = sorted(
        list(Public_Office.objects.filter(id__in=other_users_reviews_public_office_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'public_office_list': public_office_list}
    )


class SearchView(ListView):
    template_name = 'reviews/search.html'

    def search(self):

        vector = (
        SearchVector('public_office', weight='A') +
        SearchVector('comment', weight='B')+
        SearchVector('pub_date', weight='D')
        )
        query = SearchQuery('q')
        rate = SearchRank(vector, query)

        return self.get_queryset().annotate(rate=rate).filter(
        search=query).annotate(search=vector).distinct(
        'id', 'rate').order_by('-rate', 'id')


