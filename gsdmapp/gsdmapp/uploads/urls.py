from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gsdmapp.uploads.views',
    url(r'^$', 'file_upload', name='file_upload'),
)