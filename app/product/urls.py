from django.urls import path, include

from rest_framework.routers import DefaultRouter

from product import views


router = DefaultRouter()
router.register('product', views.ProductApiViewSet)
router.register('order', views.OrderApiView)

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]
