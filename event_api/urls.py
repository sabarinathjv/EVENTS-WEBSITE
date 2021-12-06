from django.urls import path , re_path
from .views import*
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('events', Eventfetch.as_view(), name='events'), 
    path('user/', Createuser.as_view(),name="create_user"),
    path('login', Login.as_view(), name='user-login'),
    path('logout', Logout.as_view(), name='user-logout'),
    path('liked', Likeapi.as_view(), name='like-fetcher'),
    re_path('^filter/(?P<startdate>.+)/(?P<enddate>.+)/(?P<category>.+)/$', Filterapi.as_view()),
]
