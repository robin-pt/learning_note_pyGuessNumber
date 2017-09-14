from django.conf.urls import url
from . import views


app_name = "gnumber"

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^create/$', views.createRoom, name='create'),
    url(r'^(?P<room_id>\w+)/game/$', views.gameRoom, name='game'),
]
