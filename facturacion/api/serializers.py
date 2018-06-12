from rest_framework import serializers
from ..models import FacturaElectronica

class FacturaElectronicaSerializer(serializers.ModelSerializer):
    class Meta:
        model= FacturaElectronica
        fields='__all__'

