from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'material_types', MaterialTypeViewSet, basename='material_types')

urlpatterns = [
    path('register_material/', registerMaterial, name='register_material'),
    path('', include(router.urls)),
]