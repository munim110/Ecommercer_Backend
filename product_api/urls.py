from rest_framework import routers
from .views import *
from django.urls import include, re_path


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='Product')
router.register(r'cart-items', CartItemViewSet, basename='Cart-Item')
router.register(r'carts', CartViewSet, basename='Cart')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]