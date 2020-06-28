from django.conf.urls import url, include
from . import views


app_name = 'accounts'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^dashboard/$', views.dashboard, name='dashboard')
]