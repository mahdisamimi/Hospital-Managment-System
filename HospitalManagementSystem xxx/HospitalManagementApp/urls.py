from django.conf.urls import url, include
from . import views

# app_name='web'
urlpatterns = [
    url('',views.index)
]
