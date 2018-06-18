from rest_framework import serializers
from ..models import FacturaElectronica , Usuario ,DetalleFacturaElectronica

class FacturaElectronicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaElectronica
        fields='__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields='__all__'

class DetalleFacturaElectronicaSerializer(serializers.ModelSerializer):
    class Meta:
        model =DetalleFacturaElectronica
        fields= '__all__'