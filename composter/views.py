from django.shortcuts import render
from django.urls import path, include
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED
)
from djongo import *
from .models import *
from .serializers import *
from bson import ObjectId

class MaterialTypeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = MaterialType.objects.all()
        serializer = MaterialTypeSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def registerMaterial(request):
    try:
        material_type_id = ObjectId(request.data['materialType'])
        material_type = MaterialType.objects.get(_id=material_type_id)
    except Exception:
        return Response(
            {'error': 'Tipo de material inválido'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        material = Material.objects.create(materialType=material_type, 
            name = request.data['name'],
            imageLink = request.data['imageLink']
        )
    except Exception:
        return Response(
            {'error': 'Erro interno do servidor'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    response_data = MaterialSerializer(material).data
    response_data['materialType'] = str(response_data['materialType'])
    return Response(
        response_data,
        status=HTTP_201_CREATED
    )