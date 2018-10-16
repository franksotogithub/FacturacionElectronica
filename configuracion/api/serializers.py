from rest_framework import serializers
from ..models import  Local ,EmpresaParametro

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'

class EmpresaParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaParametro
        fields = '__all__'