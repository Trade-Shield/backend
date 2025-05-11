from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShippingRouteViewSet

router = DefaultRouter()
router.register(r'shipping-routes', ShippingRouteViewSet, basename='shipping-routes')

urlpatterns = [
    path('', include(router.urls)),
]
