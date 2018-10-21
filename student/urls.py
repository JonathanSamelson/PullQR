from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('my', views.my, name="my"),
    path('accounts/password', views.change_password, name="password"),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)