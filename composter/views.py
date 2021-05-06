from django.shortcuts import render
from django.urls import path, include
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR,
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
            {'error': 'Tipo de material - ID inválido'},
            status=HTTP_400_BAD_REQUEST
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

@api_view(["GET"])
def materials(request):
    materials = Material.objects.all()
    response_data = MaterialSerializer(materials, many=True).data

    for each in response_data:
        each['materialType'] = str(each['materialType'])

    return Response(
        response_data,
        status=HTTP_201_CREATED
    )

@api_view(["PUT", "DELETE"])
def updateMaterial(request, id):
    try:
        material_id = ObjectId(id)
        material = Material.objects.get(_id=material_id)
    except Exception:
        return Response(
            {'error': 'Material - ID inválido'},
            status=HTTP_400_BAD_REQUEST
        )

    if request.method == "DELETE":
        material.delete()
        return Response(
            {'OK':'Deleted'},
            status=HTTP_200_OK
        )

    elif request.method == "PUT":
        try:
            if request.data['name']:
                material.name = request.data['name']
        except Exception:
            pass 

        try:
            if request.data['imageLink']:
                material.imageLink = request.data['imageLink']
        except Exception:
            pass 

        try:
            if request.data['materialType']:
                try:
                    material_type_id = ObjectId(request.data['materialType'])
                    material_type = MaterialType.objects.get(_id=material_type_id)
                except Exception:
                    return Response(
                        {'error': 'Tipo de material - ID inválido'},
                        status=HTTP_400_BAD_REQUEST
                    ) 

                material.materialType = material_type
        except Exception:
            pass 

        material.save()

        response_data = MaterialSerializer(material).data
        response_data['materialType'] = str(response_data['materialType'])

        return Response(
            response_data,
            status=HTTP_200_OK
        )
    else:
        return Response(
            {'error': 'Método não permitido'},
            status=HTTP_405_METHOD_NOT_ALLOWED
        )
