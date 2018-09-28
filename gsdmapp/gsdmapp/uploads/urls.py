from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gsdmapp.uploads.views',
    url(r'^samplingdata/$', 'sampling_file_upload', name='sampling_file_upload'),
    url(r'^adaptdata/$', 'adaptation_file_upload', name='adaptation_file_upload'),
)