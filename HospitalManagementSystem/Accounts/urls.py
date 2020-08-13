from django.conf.urls import url, include

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^add-manager/$', views.manager_signup, name='add-manager'),
    url(r'^usri/$', views.usri, name='usri'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^change-password/$', views.change_password, name='change password'),
    url(r'^modify/$', views.modify, name='modify'),
    url(r'^rezervd/$', views.rezerv, name='rezerv'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^rezerv/$', views.rezerv, name='rezerv'),
    url(r'^rezerv_list/$', views.rezerv_list, name='rezerv_list'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_rezerv, name='delete'),
    url(r'^update/(?P<id>\d+)/$', views.update_rezerv, name='update'),
    url(r'^updating/$', views.updating, name='updating'),
]
