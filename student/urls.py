from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name="index"),
    path('my', views.my, name="my"),
    path('accounts/password', views.change_password, name="password"),
    path('accounts/signup', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.activate, name='activate'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)