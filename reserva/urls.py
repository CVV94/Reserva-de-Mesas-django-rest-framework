from django.urls import path
from . import views
from .views import MesaList, MesaDetail,ReservaView

urlpatterns = [
    path("", views.index, name="index"),
    path("listadoReservas/", views.listadoReservas, name="listadoReservas"),
    path("registrarReserva/", views.registrarReserva, name="registrarReserva"),
    path("modificarReserva/<int:id>", views.modificarReserva, name="modificarReserva"),
    path("eliminarReserva/<int:id>", views.eliminarReserva, name="eliminarReserva"),
    path("registrarMesa/", views.registrarMesa, name="registrarMesa"),
    path("getReservas/", ReservaView.as_view(), name="getReservas"),
    path("getReservas/<int:id>/", ReservaView.as_view(), name="getReservasId"),
    # path("getReservas/<int:pk>",ReservaDetail.as_view(), name="crudReserva"),
    path("mesas/", MesaList.as_view(), name="listaMesas"),
    path("mesas/<int:pk>", MesaDetail.as_view(), name="detalleMesa"),
    path("modificarMesa/<int:id>", views.modificarMesa, name="modificarMesa"),
    path("eliminarMesa/<int:id>", views.eliminarMesa, name="eliminarMesa"),
    path("listadoMesas/", views.listadoMesas, name="listadoMesas"),
]
