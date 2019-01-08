"""gsdmapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin

urlpatterns = [
	url(r'^$', 'gsdmapp.views.app', name='app'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^soilmaps/$', 'gsdmapp.views.soilmaps'),
    url(r'^samplingdraw/$', 'gsdmapp.views.sampling_draw'),
    url(r'^samplingshp/$', 'gsdmapp.views.sampling_shp'),
    url(r'^localadapt/$', 'gsdmapp.views.local_adaptation'),
    url(r'^uploads/', include('gsdmapp.uploads.urls')),
    url(r'^gadm/', 'gsdmapp.views.gadm', name='gadm'),
    url(r'^level1/(?P<country>[^/]*)/$', 'gsdmapp.views.level1'),
    url(r'^level2/(?P<level1>[^/]*)/$', 'gsdmapp.views.level2'),
    url(r'^level3/(?P<level2>[^/]*)/$', 'gsdmapp.views.level3'),

]
