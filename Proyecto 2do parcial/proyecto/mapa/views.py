from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from .models import*
import pandas as pd
from .utils import get_longitude, get_latitude, get_codes, get_transport
from django.core.management import call_command
import numpy as np
from sklearn.datasets import make_blobs
from sklearn import preprocessing 
from sklearn.cluster import KMeans
from sklearn import cluster
import matplotlib.pyplot as plt

def index(request):
    call_command('add_data')
    item = Transport.objects.all().values()
    df = pd.DataFrame(item)
    mydict = {
        "df": df.to_html()
    }
    return render(request, "index.html", context=mydict)
        
def metricas(request):
    df = Transport.objects.all()
    x1 = [x.Longitude for x in df]
    x2 = [x.Latitude for x in df]
    labels1 = []
    sizes1 = []
    plot_pie(df, labels1, sizes1)

    labels2 = []
    sizes2 = []
    plot_bar(df, labels2, sizes2)

    longitude = get_longitude(x1)
    latitude = get_latitude(x2)
    code = get_codes(labels1, sizes1)
    transport = get_transport(labels2, sizes2)

    mydict = {
        'longitude': longitude, 
        'latitude': latitude,
        'code': code,
        'transport': transport
    }
    return render (request, 'metricas.html', context=mydict)

def plot_pie(df, labels, sizes):
    x = [x.Code for x in df]
    my_dict = {i:x.count(i) for i in x}

    for x, y in my_dict.items():
        labels.append(x)
        sizes.append(y)

def plot_bar(df, labels, sizes):
    x = [x.Transport for x in df]
    my_dict = {i:x.count(i) for i in x}

    for x, y in my_dict.items():
        labels.append(x)
        sizes.append(y)

def mapa(request):
    call_command('add_data')
    item = Transport.objects.all().values()
    mydict = {
        "item": item
    }
    return render(request, "map.html", context=mydict)

def mapaPoblaciones(request):
    item = Poblaciones.objects.all().values()
    mydict = {
        "item": item
    }
    return render(request, "mapaPoblaciones.html", context=mydict)

def agregarPoblacion(request, RLongitudMin, RLongitudMax, RLatitudMin, RLatitudMax, NPuntos, Dispersion):
    RLongitudMin = float(RLongitudMin)
    RLongitudMax = float(RLongitudMax)
    RLatitudMin = float(RLatitudMin)
    RLatitudMax = float(RLatitudMax)
    Dispersion = float(Dispersion)
    coordinates, y = make_blobs(n_samples = NPuntos,n_features = 1,cluster_std = Dispersion, shuffle = False, center_box = (RLongitudMin,RLongitudMax))
    coordinates1, y = make_blobs(n_samples = NPuntos,n_features = 1,cluster_std = Dispersion, shuffle = False, center_box = (RLatitudMin,RLatitudMax))
    coordinates = np.append(coordinates,coordinates1,axis=1)

    listaPoblacion = []
    for x in coordinates:
        poblacion = Poblaciones(
            Longitud = x[1],
            Latitud = x[0]
        )
        listaPoblacion.append(poblacion)

    Poblaciones.objects.bulk_create(listaPoblacion)
     
    return redirect('mapaPoblaciones')

def wipePoblacion(request):
    Poblaciones.objects.all().delete()
    return redirect('mapaPoblaciones')

def customMap(request):
    item = Poblaciones.objects.all().values()
    mydict = {
        "item": item
    }
    return render(request, "customMap.html", context=mydict)

def crearClusters(request, NClusters, Tolerancia, NIteraciones):
    NClusters = int(NClusters)
    NIteraciones = int(NIteraciones)
    Tolerancia = float(Tolerancia)

    item = Poblaciones.objects.all().values()
    df = pd.DataFrame(item)
    #print(df)
    df = df.drop('id', 1)
    #print(df)

    x = df['Longitud'].values
    y = df['Latitud'].values

    kmeans = [KMeans(n_clusters=i) for i in range(NIteraciones)]
    kmeans = KMeans(n_clusters=NClusters).fit(df)
    centroids = kmeans.cluster_centers_
    print(centroids)
    labels = kmeans.predict(df)
    df['label'] = labels
    print(df)

    colores=['red','green','blue','yellow','fuchsia', 'orange', 'peru', 'deeppink', 'teal', 'grey']
    asignar=[]
    for row in labels:
        asignar.append(colores[row])

    img = plt.imread("../mapa.png")
    #fig, ax = plt.subplots()
    fig = plt.figure()
    fig.set_figheight(6)
    fig.set_figwidth(10)
    plt.imshow(img, extent=[(df.Latitud.min()), (df.Latitud.max()), df.Longitud.min(), df.Longitud.max()])
    plt.scatter(y, x, c=asignar, s=2)
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', c='black', s=20)
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Clusters')
    plt.show()
     
    return redirect('customMap')