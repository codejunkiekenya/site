from django.conf.urls import url
from . import views

urlpatterns = [
  
    url(r'^$', views.review_list, name='review_list'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    url(r'^kenya/$', views.parks_list, name='parks_list'),
    url(r'^kenya/(?P<parks_id>[0-9]+)/$', views.parks_detail, name='parks_detail'),
    url(r'^kenya/(?P<parks_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]