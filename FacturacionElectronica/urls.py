"""FacturacionElectronica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from qr_code import urls as qr_code_urls
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^qr_code/', include(qr_code_urls, namespace="qr_code")),
    url(r'^facturacion/', include('facturacion.urls',namespace='facturacion')),
    url(r'^facturacion-api/', include('facturacion.api.urls',namespace='facturacion-api')),
    url(r'^usuarios/', include('usuarios.urls',namespace='usuarios')),
    url(r'^resumenes/', include('resumenes.urls',namespace='resumenes')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
