from . import views
from django.urls import path

urlpatterns = [
    path('', views.index , name='home'),
    path('signup', views.signup , name='signup'),
    path('signin', views.signin , name='signin'),
    path('settings', views.settings , name='settings'),
    path('logout', views.logout , name="logout"),
    path('upload', views.upload , name="upload"),

]
