"""djangoldp project URL Configuration"""
from django.conf.urls import url
from .views import ExpositionsByUser, MaterialsByUser

urlpatterns = [
    url(r'^user/(?P<username>.+)/expos/', ExpositionsByUser.urls(model_prefix="user-expositions")),
    url(r'^user/(?P<username>.+)/materiels/', MaterialsByUser.urls(model_prefix="user-materials")),
]