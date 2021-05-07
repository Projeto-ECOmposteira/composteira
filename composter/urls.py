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
    path('', include(router.urls)),
    url(r'update_material/(?P<id>[A-Za-z0-9]+)$', updateMaterial, name='update-material'),
    url(r'update_composter/(?P<id>[A-Za-z0-9]+)$', updateComposter, name='update-composter'),
]