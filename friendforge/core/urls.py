from . import views
from django.urls import path

urlpatterns = [
    path('', views.index , name='home'),
    path('signup', views.signup , name='signup'),
    path('signin', views.signin , name='signin'),
    path('settings', views.settings , name='settings'),
    path('follow', views.follow , name='follow'),
    path('logout', views.logout , name="logout"),
    path('upload', views.upload , name="upload"),
    path('profile/<str:pk>', views.profile , name="profile"),
    path('like-post', views.like_post , name="like-post"),
    path('search', views.search , name="search"),

]
