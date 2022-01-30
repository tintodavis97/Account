from django.urls import include, path
from rest_framework.routers import SimpleRouter

from myapp import views

router = SimpleRouter()

router.register('account', views.AccountViewSet, basename='account')
router.register('item', views.ItemViewSet, basename='item')
router.register('item-share', views.ItemShareViewSet, basename='item-share')

urlpatterns = [
    path('', include(router.urls)),
    path('', views.AccountViewSet, name='create-posts'),
]
