from django.shortcuts import render,HttpResponse
from appORM.models import *
from django.http import JsonResponse
from django.db.models import Q,Sum, Max, Count, Avg
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings


# Create your views here.
#consultas a realizar
#1. Cantidad de productos vendidos por Categoria

def consultas(request):
    resultado=Categoria.objects.all().values()

    return HttpResponse(resultado)


#2. Valor total de venta por producto
#3. Valor total de Venta por Categoria
#4. Promedio de Ventas por mes
#5. Máximo valor de una venta
#6. Minimo valor de una venta
#7. Cantidad mayor de un producto vendido

# def grafica1(request):
#     meses = np.array(["Enero","Febrero","Marzo"])
#     ventas = np.array(["1500000","2000000","3000000"])

#     plt.title("Ventas primer mes")
#     plt.xlabel("Meses")
#     plt.ylabel("Valor Ventas")

#     plt.bar(meses,ventas)

#     rutaImagen = os.path.join(settings.MEDIA_ROOT+"\\"+"grafica.png")

#     plt.savefig(rutaImagen)

#     return render(request,"graficas.html")

def grafica2(request):
    diaSemana = ["Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado"]

    consulta = DetalleVenta.objects.values('detVenta__venFecha__week_day').annotate(TotalVentasDia=Sum('detValorDetalle'))

    consultaCategoria = DetalleVenta.objects.values('detProducto__proCategoria__catNombre').annotate(totalVentasXCategoria=Sum('detValorDetalle'))

    xDia=[]
    y=[]
    for datos in consulta:
        mes=datos['detVenta__venFecha__week_day']
        xDia.append(diaSemana[mes-1])
        y.append(datos['TotalVentasDia'])

    plt.title("Ventas totales por día de la semana")
    
    plt.subplot(2, 1, 1)
    plt.pie(y, labels=xDia)

    #tabla #2
    xCategorias=[]
    yVentasCategorias=[]

    for datos in consultaCategoria:
        xCategorias.append(datos['detProducto__proCategoria__catNombre'])
        yVentasCategorias.append(datos['totalVentasXCategoria'])

    plt.subplot(2, 1, 2)
    plt.bar(xCategorias,yVentasCategorias)

    rutaImagen = os.path.join(settings.MEDIA_ROOT+"\\"+"grafica.png")
    plt.savefig(rutaImagen)
    return render(request,"graficas.html")
    

def graficaGoogle(request):
    return render(request,"graficasGoogle.html")

def googleGrafica(request):
    return render(request,"googleGrafica.html")


def grafica1Google(request):
    ventasProducto = DetalleVenta.objects.values('detProducto').\
        annotate(TotalVentaProducto=Sum('detValorDetalle'))
    listaDatos=[]
    listaDatos.append(['Producto','ValorVenta'])

    for ventaProducto in ventasProducto:
        producto=Producto.objects.get(pk=ventaProducto['detProducto']).proNombre
        valorVenta=ventaProducto['TotalVentaProducto']
        listaDatos.append([producto,valorVenta])
    retorno={'datos':listaDatos}

    return JsonResponse(retorno)