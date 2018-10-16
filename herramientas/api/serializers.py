from rest_framework import serializers
from herramientas.models import Proceso
from rest_framework.fields import ChoiceField

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields= '__all__'