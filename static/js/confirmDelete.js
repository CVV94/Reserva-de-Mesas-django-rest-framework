function confirmDelete(id) {
    var r = confirm("¿Estás seguro de que quieres eliminar esta reserva?");
    if (r == true) {
        // Si el usuario confirma, redirige al usuario a la URL que maneja la eliminación de la reserva.
        window.location.href = "{% url 'eliminarReserva' 'id_placeholder' %}".replace('id_placeholder', id);
    }
}
