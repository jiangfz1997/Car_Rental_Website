"""Proj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.views.static import serve
from . import settings
from Proj2 import settings
from func import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name='polls'
urlpatterns=[
    url(r'^admin/', admin.site.urls),
    url(r'^index/', admin.site.urls),
    #url(r'^login/', views.login_view),
    #url(r'^test/',views.test),
    #url(r'^register/registerIndi',views.test),
    url(r'^$', views.index),
    url(r'^registerIndi/', views.registerIndi),
    url(r'^registerCorp/', views.registerCorp),
    url(r'^register/', views.register),
    #url(r'^logout/', views.logout_view),
    #url(r'^profile/', views.profile),
    url(r'^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
urlpatterns += staticfiles_urlpatterns()