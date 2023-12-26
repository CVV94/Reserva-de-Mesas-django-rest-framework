from django.shortcuts import render, redirect
from .models import Mesa, Reserva
from .forms import ReservaForm, MesaForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReservaSerializer, MesaSerializer
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'index.html')

def listadoReservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'listadoReservas.html', {'reservas':reservas})

def listadoMesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'listadoMesas.html', {'mesas':mesas})

def modificarMesa(request, id):
    mesa = Mesa.objects.get(id=id)
    form = MesaForm(instance=mesa)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            mensaje = "Mesa modificada correctamente"
            return redirect('listadoMesas')
    return render(request, 'registrarMesa.html', {'form':form, 'editando':True})

def eliminarMesa(request, id):
    mesa = Mesa.objects.get(id=id)
    mesa.delete()
    return redirect('listadoMesas')

def registrarReserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            cantidad_personas = form.cleaned_data.get('cantidad_personas')
            mesas_disponibles = Mesa.objects.filter(capacidad_personas__gte=cantidad_personas)
            if not mesas_disponibles:
                form.add_error('cantidad_personas', 'No hay mesas disponibles que puedan soportar esta cantidad de personas.')
            else:
                form.save()
                mensaje = "Reserva registrada correctamente"
                return render(request, 'registrarReserva.html', {'form':form, 'mensaje':mensaje})
    else:
        form = ReservaForm()
    return render(request, 'registrarReserva.html', {'form':form, 'editando':False})

def modificarReserva(request, id):
    reserva = Reserva.objects.get(id=id)
    form = ReservaForm(instance=reserva)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            mensaje = "Reserva modificada correctamente"
            return redirect('listadoReservas')
    return render(request, 'registrarReserva.html', {'form':form, 'editando':True})

def eliminarReserva(request, id):
    reserva = Reserva.objects.get(id=id)
    reserva.delete()
    return redirect('listadoReservas')

def registrarMesa(request):
    form= MesaForm()
    if request.method == 'POST':
        numero = request.POST.get('numero')
        capacidad_personas = request.POST.get('capacidad_personas')
        mesa = Mesa(numero=numero, capacidad_personas=capacidad_personas)
        mesa.save()
        mensaje = "Mesa registrada correctamente"
        return render(request, 'registrarMesa.html', {'mensaje':mensaje, 'form':form})
    return render(request, 'registrarMesa.html', {'form':form})

# @api_view(['GET', 'POST'])
# def getReservas(request):
#     if request.method=='GET':
#         reservas = Reserva.objects.all().order_by('fecha_reserva')
#         serializer = ReservaSerializer(reservas, many=True)
#         return Response(serializer.data)

#     if request.method=='POST':
#         serializer = ReservaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ReservaFilter(filters.FilterSet):
    class Meta:
        model = Reserva
        fields = ['id']

# class ReservaList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Reserva.objects.all().order_by('fecha_reserva')
#     serializer_class = ReservaSerializer
#     filterset_class = ReservaFilter

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
    
# class ReservaDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Reserva.objects.all()
#     serializer_class = ReservaSerializer
        
class ReservaView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Reserva.objects.all().order_by('fecha_reserva')
    serializer_class = ReservaSerializer
    filterset_class = ReservaFilter
    lookup_field = 'id'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.query_params.get('id'))
        return obj

    def get(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id is not None:
            reserva = Reserva.objects.filter(id=id).first()
            if reserva:
                serializer = ReservaSerializer(reserva)
                return Response(serializer.data)
            else:
                return Response({"error": "No reserva found with provided id"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return self.list(request, *args, **kwargs)
        
    def put(self, request, *args, **kwargs):
            id = request.query_params.get('id', None)
            if id is not None:
                reserva = Reserva.objects.filter(id=id).first()
                if reserva:
                    serializer = ReservaSerializer(reserva, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "No reserva found with provided id"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "No id provided"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id is not None:
            Reserva.objects.filter(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "No id provided"}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def crudReserva(request, id):
#     reserva = Reserva.objects.get(id=id)
#     if request.method=='GET':
#         serializer = ReservaSerializer(reserva)
#         return Response(serializer.data)
    
#     if request.method=='PUT':
#         serializer = ReservaSerializer(reserva, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method=='DELETE':
#         reserva.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    

# class MesaList(APIView):
#     def get(self, request, format=None):
#         mesas = Mesa.objects.all()
#         serializer = MesaSerializer(mesas, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = MesaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# /mesas/?numero=5
class MesaFilter(filters.FilterSet):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad_personas']
    
class MesaList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    filterset_class = MesaFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
 
class MesaDetail(APIView):
    def get_object(self, pk):
        try:
            return Mesa.objects.get(pk=pk)
        except Mesa.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk, format=None):
        mesa = self.get_object(pk)
        serializer = MesaSerializer(mesa)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        mesa = self.get_object(pk)
        serializer = MesaSerializer(mesa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        mesa = self.get_object(pk)
        mesa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)