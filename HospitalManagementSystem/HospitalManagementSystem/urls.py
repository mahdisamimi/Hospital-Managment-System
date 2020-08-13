"""HospitalManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Accounts import views
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import reverse_lazy

urlpatterns = [
    url(r'^permission-denied/$', views.permission_denied, name='permission denied'),
    url('admin/', admin.site.urls),
    url(r'^accounts/', include('Accounts.urls', namespace='accounts'), name='accounts'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    url('', include('HospitalManagementApp.urls')),
    url('^', include('django.contrib.auth.urls')),
]
urlpatterns += staticfiles_urlpatterns()
