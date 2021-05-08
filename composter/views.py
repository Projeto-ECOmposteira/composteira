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
import json
from bson import json_util

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
            {'error': 'Atributos obrigatórios: name, imageLink'},
            status=HTTP_400_BAD_REQUEST
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
        status=HTTP_200_OK
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
        if request.data.get('name', None):
                material.name = request.data['name']

        if request.data.get('imageLink', None):
                material.imageLink = request.data['imageLink']
                
        if request.data.get('imageLink', None):
            try:
                material_type_id = ObjectId(request.data['materialType'])
                material_type = MaterialType.objects.get(_id=material_type_id)
            except Exception:
                return Response(
                    {'error': 'Tipo de material - ID inválido'},
                    status=HTTP_400_BAD_REQUEST
                ) 

            material.materialType = material_type


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

@api_view(["POST"])
def registerComposter(request):
    try:
        composter = Composter.objects.create( 
            supermarketId = request.data['supermarketId'],
            macAddress = request.data['macAddress'],
            name = request.data['name'],
            description = request.data['description'],
        )
    except Exception:
        return Response(
            {'error': 'Atributos obrigatórios: supermarketId, name, macAddress, description'},
            status=HTTP_400_BAD_REQUEST 
        )
    
    response_data = ComposterSerializer(composter).data
    return Response(
        response_data,
        status=HTTP_201_CREATED
    )

@api_view(["PUT", "DELETE"])
def updateComposter(request, id):
    try:
        composter_id = ObjectId(id)
        composter = Composter.objects.get(_id=composter_id)
    except Exception:
        return Response(
            {'error': 'Composteira - ID inválido'},
            status=HTTP_400_BAD_REQUEST
        )
    if request.method == "DELETE":
        if not composter.isActive:
            return Response(
                {'error':'Composteira não está ativa'},
                status=HTTP_400_BAD_REQUEST
            )

        composter.isActive = False
        composter.save()
        return Response(
            {'OK':'Deleted'},
            status=HTTP_200_OK
        )

    elif request.method == "PUT":
        if request.data.get('name', None):
            composter.name = request.data['name']

        if request.data.get('macAddress', None):
                composter.macAddress = request.data['macAddress']

        if request.data.get('description', None):
                composter.description = request.data['description']

        if request.data.get('supermarketId', None):
                composter.supermarketId = request.data['supermarketId']

        composter.save()

        response_data = ComposterSerializer(composter).data

        return Response(
            response_data,
            status=HTTP_200_OK
        )
    else:
        return Response(
            {'error': 'Método não permitido'},
            status=HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(["POST"])
def getProducerComposters(request):
    producer_supermarkets = json.loads(request.data['markets'])

    composters = []
    for each in producer_supermarkets:
        each_composters = Composter.objects.filter(supermarketId = each['pk'])
        each_composters = ComposterSerializer(each_composters, many=True).data
        for i in each_composters:
            i['supermarketEmail'] = each['email']
        composters.append(each_composters)

    return Response(
            composters,
            status=HTTP_200_OK
        )

@api_view(["POST"])
def getSupermarketComposters(request):

    composters = Composter.objects.filter(supermarketId = request.data['pk'])
    composters = ComposterSerializer(composters, many=True).data

    return Response(
            composters,
            status=HTTP_200_OK
        )

@api_view(["POST"])
def getComposterAlerts(request):
    producer_supermarkets = json.loads(request.data['markets'])

    composters = []
    for each in producer_supermarkets:
        each_composters = Composter.objects.filter(supermarketId = each['pk'])
        each_composters = ComposterSerializer(each_composters, many=True).data
        for i in each_composters:
            i['supermarketEmail'] = each['email']
        composters.append(each_composters)

    alerts = []

    for composter in composters:
        for each in composter:
            _composter = Composter.objects.get(_id = ObjectId(each['_id']))

            each_alerts = Alert.objects.filter(composter = _composter, endDate = None)
            each_alerts = AlertSerializer(each_alerts, many=True).data

            for _alert in each_alerts:
                _alert['composter'] = ComposterSerializer(_composter).data       
            
            alerts.append(each_alerts)


    return Response(
            json.loads(json_util.dumps(alerts)),
            status=HTTP_200_OK
        )