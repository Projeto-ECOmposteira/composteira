from rest_framework import serializers
from .models import *

class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = ('__all__')
        
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('__all__')

    def create(self, validated_data):
        material = Material.objects.create(
            name=validated_data['name'],
            imageLink=validated_data['imageLink'],
            materialType=validated_data['materialType'],
        )

        return material
