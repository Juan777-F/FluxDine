// ── CSRF token ───────────────────────────────────────────────
let CSRF = '';
document.addEventListener('DOMContentLoaded', () => {
    CSRF = document.querySelector('#form-editar [name=csrf_token]')?.value || '';
});


// ── Modal editar ─────────────────────────────────────────────
function abrirModal(id) {
    fetch(`/admin/inventario/editar/${id}`)
        .then(r => r.json())
        .then(d => {
            document.getElementById('edit-id').value           = d.id;
            document.getElementById('edit-nombre').value       = d.nombre;
            document.getElementById('edit-categoria').value    = d.categoria_id;
            document.getElementById('edit-descripcion').value  = d.descripcion;
            document.getElementById('edit-precio').value       = d.precio_venta;
            document.getElementById('edit-stock-actual').value = d.stock_actual;
            document.getElementById('edit-stock-minimo').value = d.stock_minimo;
            document.getElementById('edit-estado').value       = d.estado;
            document.getElementById('modal-editar').style.display = 'flex';
        })
        .catch(() => {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo cargar el producto.',
                confirmButtonColor: '#e74c3c'
            });
        });
}

function cerrarModal() {
    document.getElementById('modal-editar').style.display = 'none';
}

// Cerrar con clic fuera del modal
document.getElementById('modal-editar').addEventListener('click', function(e) {
    if (e.target === this) cerrarModal();
});

// Submit editar — guarda con AJAX y muestra SweetAlert
document.getElementById('form-editar').addEventListener('submit', function(e) {
    e.preventDefault();
    const id   = document.getElementById('edit-id').value;
    const data = new FormData(this);

    fetch(`/admin/inventario/editar/${id}`, { method: 'POST', body: data })
        .then(r => r.json())
        .then(d => {
            cerrarModal();
            if (d.ok) {
                Swal.fire({
                    icon: 'success',
                    title: '¡Guardado!',
                    text: d.mensaje,
                    confirmButtonColor: '#e74c3c',
                    timer: 2000,
                    timerProgressBar: true
                }).then(() => location.reload());
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al guardar',
                    text: d.mensaje,
                    confirmButtonColor: '#e74c3c'
                });
            }
        })
        .catch(() => {
            cerrarModal();
            Swal.fire({
                icon: 'error',
                title: 'Error de conexión',
                text: 'No se pudo guardar el producto. Intenta de nuevo.',
                confirmButtonColor: '#e74c3c'
            });
        });
});


// ── Eliminar — confirmación con SweetAlert ───────────────────
function eliminarProducto(id, nombre) {
    Swal.fire({
        title: '¿Eliminar producto?',
        html: `Se eliminará <strong>${nombre}</strong> permanentemente.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e74c3c',
        cancelButtonColor: '#6b7280',
        confirmButtonText: '<i class="bi bi-trash"></i> Sí, eliminar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then(result => {
        if (!result.isConfirmed) return;

        const data = new FormData();
        data.append('csrf_token', CSRF);

        fetch(`/admin/inventario/eliminar/${id}`, { method: 'POST', body: data })
            .then(r => r.json())
            .then(d => {
                if (d.ok) {
                    // Animar salida de la fila
                    const fila = document.getElementById(`fila-${id}`);
                    if (fila) {
                        fila.style.transition = 'opacity 0.4s, transform 0.4s';
                        fila.style.opacity    = '0';
                        fila.style.transform  = 'translateX(30px)';
                        setTimeout(() => fila.remove(), 420);
                    }
                    Swal.fire({
                        icon: 'success',
                        title: 'Eliminado',
                        text: d.mensaje,
                        confirmButtonColor: '#e74c3c',
                        timer: 2000,
                        timerProgressBar: true
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'No se pudo eliminar',
                        text: d.mensaje,
                        confirmButtonColor: '#e74c3c'
                    });
                }
            })
            .catch(() => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error de conexión',
                    text: 'No se pudo eliminar el producto. Intenta de nuevo.',
                    confirmButtonColor: '#e74c3c'
                });
            });
    });
}