from django.urls import path, include
from django.conf.urls import url
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'material_types', MaterialTypeViewSet, basename='material_types')

urlpatterns = [
    path('register_material/', registerMaterial, name='register-material'),
    path('materials/', materials, name='materials-list'),
    path('register_composter/', registerComposter, name='register-composter'),
    path('get_producer_composters/', getProducerComposters, name='get-producer-composters'),
    path('get_supermarket_composters/', getSupermarketComposters, name='get-supermarket-composters'),
    path('get_composter_alerts/', getComposterAlerts, name='get-composter-alerts'),
    path('', include(router.urls)),
    url(r'update_material/(?P<id>[A-Za-z0-9]+)$', updateMaterial, name='update-material'),
    url(r'update_composter/(?P<id>[A-Za-z0-9]+)$', updateComposter, name='update-composter'),
    url(r'get_composter_report/(?P<id>[A-Za-z0-9]+)$', getComposterReport, name='get-composter-report'),
]

from . import mqtt

mqtt.client.loop_start()