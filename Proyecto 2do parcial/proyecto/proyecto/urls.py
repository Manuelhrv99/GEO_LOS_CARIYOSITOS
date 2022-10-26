"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from mapa import views

# Para la cuenta de admin
# Usuario: mhrv9
# Contraseña: root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('metricas', views.metricas, name='metricas'),
    path('mapa', views.mapa, name='mapa'),
    path('mapaPoblaciones', views.mapaPoblaciones, name='mapaPoblaciones'),
    path('agregarPoblacion/<str:RLongitudMin>/<str:RLongitudMax>/<str:RLatitudMin>/<str:RLatitudMax>/<int:NPuntos>/<str:Dispersion>', views.agregarPoblacion, name='agregarPoblacion'),
    path('wipePoblacion', views.wipePoblacion, name='wipePoblacion'),
    path('customMap', views.customMap, name='customMap'),
    path('crearClusters/<str:NClusters>/<str:NIteraciones>/<str:Tolerancia>', views.crearClusters, name='crearClusters'),
]
