from django.conf.urls import url

from .views import my_profile,ProductDownloadView

app_name = 'accounts'

urlpatterns = [
	url(r'^profile/$', my_profile, name='my_profile'),
	url(r'^(?P<slug>[\w-]+)/download/$', ProductDownloadView.as_view(), name='download_slug'),
]
