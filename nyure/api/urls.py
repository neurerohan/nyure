from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vegetables', views.VegetableViewSet)

urlpatterns = [
    path('trigger-scrape/', views.trigger_scraping, name='trigger_scraping'),
    path('', include(router.urls)),
    path('scrape/', views.trigger_scrape, name='trigger-scrape'),
]
