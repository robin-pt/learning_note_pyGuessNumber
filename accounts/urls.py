""" Guess number accounts urls """

from django.conf.urls import url
from django.contrib.auth import views as generic_user_views
from . import views


app_name = "accounts"

urlpatterns = [
    url(r'^login/$', views.Signin.as_view(), name='user_login'),
    url(r'^logout/$', generic_user_views.logout_then_login, name='user_logout'),
    url(r'^signup/$', views.singup, name='user_signup'),
]
