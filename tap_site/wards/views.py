from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Review, Wards, Cluster, Preference
from .forms import ReviewForm
from .suggestions import update_clusters
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


@cache_page(10 * 1)
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/wards/review_list.html', context)

@cache_page(10 * 1)
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/wards/review_detail.html', {'review': review})


def wards_list(request):
    wards_list = Wards.objects.order_by('-name')
    context = {'wards_list':wards_list}
    return render(request, 'reviews/wards/wards_list.html', context)

@cache_page(10 * 1)
def wards_detail(request, wards_id):
    wards = get_object_or_404(Wards, pk=wards_id)
    form = ReviewForm()
    return render(request, 'reviews/wards/wards_detail.html', {'wards': wards,'form': form})

@login_required
def add_review(request, wards_id):
    if request.method == "POST":
        wards = get_object_or_404(Wards, pk=wards_id)
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            image = form.cleaned_data['image']
            user_name = request.user.username
            review = Review()
            review.wards = wards
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
            return HttpResponseRedirect(reverse('wards:wards_detail', args=(wards.id,)))
    else:
        form = ReviewForm()

    return render(request, 'reviews/wards/wards_detail.html', {'form': form})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)

@login_required
def user_recommendation_list(request):
    
    # get request user reviewed offices
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wards')
    user_reviews_wards_ids = set(map(lambda x: x.wards.id, user_reviews))

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
            .exclude(wards__id__in=user_reviews_wards_ids)
    other_users_reviews_wards_ids = set(map(lambda x: x.wards.id, other_users_reviews))
    
    # then get a offices list including the previous IDs, order by rating
    wards_list = sorted(
        list(Wards.objects.filter(id__in=other_users_reviews_wards_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'wards_list': wards_list}
    )

@login_required
def postpreference(request, review_id, userpreference):
        
        if request.method == "POST":
                review= get_object_or_404(Review, id=review_id)

                obj=''

                valueobj=''

                try:
                        obj= Preference.objects.get(user= request.user, review= review)

                        valueobj= obj.value #value of userpreference


                        valueobj= int(valueobj)

                        userpreference= int(userpreference)
                
                        if valueobj != userpreference:
                                obj.delete()


                                upref= Preference()
                                upref.user= request.user

                                upref.review= review

                                upref.value= userpreference


                                if userpreference == 1 and valueobj != 1:
                                        review.likes += 1
                                        review.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        review.dislikes += 1
                                        review.likes -= 1
                                

                                upref.save()

                                review.save()
                        
                        
                                context= {'review': review,
                                  'review_id': review_id}

                                return render (request, 'reviews/wards/review_detail.html', context)

                        elif valueobj == userpreference:
                                obj.delete()
                        
                                if userpreference == 1:
                                        review.likes -= 1
                                elif userpreference == 2:
                                        review.dislikes -= 1

                                review.save()

                                context= {'review': review,
                                  'review_id': review_id}

                                return render (request, 'reviews/wards/review_detail.html', context)
                                
                        
        
                
                except Preference.DoesNotExist:
                        upref= Preference()

                        upref.user= request.user

                        upref.review= review

                        upref.value= userpreference

                        userpreference= int(userpreference)

                        if userpreference == 1:
                                review.likes += 1
                        elif userpreference == 2:
                                review.dislikes +=1

                        upref.save()

                        review.save()                            


                        context= {'review': review,
                          'review_id': review_id}

                        return render (request, 'reviews/wards/review_detail.html', context)


        else:
                review= get_object_or_404(Review, id=review_id)
                context= {'review': review,
                          'review_id': review_id}

                return render (request, 'reviews/wards/review_detail.html', context)


def search(self):
    qs = Review.objects.filter(visible=True)
    vector = (
        SearchVector('public_office') +
        SearchVector('comment')
        )
    query = self.request.GET['q']
    qs = qs.annotate(search=vector).filter(search=query).order_by('pub_date')

    return qs
# Create your views here.
