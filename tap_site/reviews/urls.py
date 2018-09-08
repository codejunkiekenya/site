from django.conf.urls import url, include
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /public_office/
    url(r'^kenya$', views.public_office_list, name='public_office_list'),
    # ex: /public_office/5/
    url(r'^kenya/(?P<public_office_id>[0-9]+)/$', views.public_office_detail, name='public_office_detail'),
    url(r'^kenya/(?P<public_office_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
    # ex: /search results
    #url(r'^search-results/$', views.search, name='search'),
    url(r'^search/', views.SearchView.as_view(), name='search'),
    #url(r'^author/((?P<pk>\d+)/$', PublicOfficeView.as_view(), name='author_detail'),
]