from rest_framework import routers
from . import views
from django.urls import include, re_path

router = routers.DefaultRouter()
router.register(r'users', views.UserViewset)
router.register(r'change-password', views.ChangePasswordView, basename='Change-Password')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]