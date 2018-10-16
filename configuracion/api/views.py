from .serializers import LocalSerializer , EmpresaParametroSerializer
from ..models import Local , EmpresaParametro
from rest_framework.viewsets import ViewSet, ModelViewSet

class LocalViewSet(ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

class EmpresaParametroViewSet(ModelViewSet):
    queryset = EmpresaParametro.objects.all()
    serializer_class = EmpresaParametroSerializer

