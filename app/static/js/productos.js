// ═══════════════════════════════════════════════════════════════
//  productos.js — Módulo Catálogo / Carta de La Pikda
// ═══════════════════════════════════════════════════════════════

// ── CSRF tokens ──────────────────────────────────────────────
let CSRF_N = '', CSRF_E = '', CSRF_C = '';
document.addEventListener('DOMContentLoaded', () => {
    CSRF_N = document.querySelector('#form-nuevo  [name=csrf_token]')?.value || '';
    CSRF_E = document.querySelector('#form-editar [name=csrf_token]')?.value || '';
    CSRF_C = document.querySelector('#form-nueva-cat [name=csrf_token]')?.value || '';

    // Restaurar vista guardada
    const vista = localStorage.getItem('pikda_prod_vista') || 'tabla';
    aplicarVista(vista, false);
});


// ═══════════════════════════════════════════════════════════════
//  TOGGLE VISTA — tabla / cards
// ═══════════════════════════════════════════════════════════════

function setVista(v) {
    localStorage.setItem('pikda_prod_vista', v);
    aplicarVista(v, true);
}

function aplicarVista(v, animado) {
    const tabla = document.getElementById('vista-tabla');
    const cards = document.getElementById('vista-cards');
    const btnT = document.getElementById('btn-vista-tabla');
    const btnC = document.getElementById('btn-vista-cards');

    if (v === 'cards') {
        tabla.style.display = 'none';
        cards.style.display = 'block';
        btnT.classList.remove('active');
        btnC.classList.add('active');
    } else {
        tabla.style.display = 'block';
        cards.style.display = 'none';
        btnT.classList.add('active');
        btnC.classList.remove('active');
    }
}


// ═══════════════════════════════════════════════════════════════
//  TOGGLE DESTACADO — botón estrella
// ═══════════════════════════════════════════════════════════════

function toggleDestacado(id, btn) {
    const data = new FormData();
    data.append('csrf_token', CSRF_E || CSRF_N);

    fetch(`/admin/productos/${id}/destacar`, { method: 'POST', body: data })
        .then(r => r.json())
        .then(d => {
            if (!d.ok) return;

            // Actualizar icono del botón pulsado (puede estar en tabla o card)
            const iconos = document.querySelectorAll(
                `#fila-${id} .btn-star i, #card-${id} .btn-star-card i`
            );
            const btns = document.querySelectorAll(
                `#fila-${id} .btn-star, #card-${id} .btn-star-card`
            );

            iconos.forEach(i => {
                i.className = d.destacado ? 'bi bi-star-fill' : 'bi bi-star';
            });
            btns.forEach(b => {
                b.classList.toggle('activo', d.destacado);
            });

            // Toast pequeño sin modal completo
            mostrarToastRapido(d.destacado ? '⭐ ' + d.mensaje : d.mensaje);
        })
        .catch(() => {
            Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo actualizar.', confirmButtonColor: '#e74c3c' });
        });
}

function mostrarToastRapido(msg) {
    const t = Object.assign(document.createElement('div'), {
        className: 'swal2-container swal2-top-end swal2-fade swal2-shown',
    });
    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: msg,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        customClass: { popup: 'swal2-toast' }
    });
}


// ═══════════════════════════════════════════════════════════════
//  MODAL — NUEVO PRODUCTO
// ═══════════════════════════════════════════════════════════════

function abrirModalNuevo() {
    document.getElementById('form-nuevo').reset();
    document.getElementById('modal-nuevo').style.display = 'flex';
}

function cerrarModalNuevo() {
    document.getElementById('modal-nuevo').style.display = 'none';
}

document.getElementById('modal-nuevo').addEventListener('click', function (e) {
    if (e.target === this) cerrarModalNuevo();
});

document.getElementById('form-nuevo').addEventListener('submit', function (e) {
    e.preventDefault();
    const data = new FormData(this);

    fetch('/admin/productos/crear', { method: 'POST', body: data })
        .then(r => r.json())
        .then(d => {
            cerrarModalNuevo();
            if (d.ok) {
                Swal.fire({
                    icon: 'success', title: '¡Creado!', text: d.mensaje,
                    confirmButtonColor: '#e74c3c', timer: 2000, timerProgressBar: true
                }).then(() => location.reload());
            } else {
                Swal.fire({ icon: 'error', title: 'Error', text: d.mensaje, confirmButtonColor: '#e74c3c' });
            }
        })
        .catch(() => {
            cerrarModalNuevo();
            Swal.fire({ icon: 'error', title: 'Error de conexión', text: 'Intenta de nuevo.', confirmButtonColor: '#e74c3c' });
        });
});


// ═══════════════════════════════════════════════════════════════
//  MODAL — EDITAR PRODUCTO
// ═══════════════════════════════════════════════════════════════

function abrirModalEditar(id) {
    fetch(`/admin/productos/editar/${id}`)
        .then(r => r.json())
        .then(d => {
            document.getElementById('edit-id').value = d.id;
            document.getElementById('edit-nombre').value = d.nombre;
            document.getElementById('edit-categoria').value = d.categoria_id;
            document.getElementById('edit-descripcion').value = d.descripcion;
            document.getElementById('edit-precio').value = d.precio_venta;
            document.getElementById('edit-stock-actual').value = d.stock_actual;
            document.getElementById('edit-stock-minimo').value = d.stock_minimo;
            document.getElementById('edit-estado').value = d.estado;
            document.getElementById('edit-imagen').value = d.imagen_url || '';
            document.getElementById('modal-editar').style.display = 'flex';
        })
        .catch(() => {
            Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo cargar el producto.', confirmButtonColor: '#e74c3c' });
        });
}

function cerrarModalEditar() {
    document.getElementById('modal-editar').style.display = 'none';
}

document.getElementById('modal-editar').addEventListener('click', function (e) {
    if (e.target === this) cerrarModalEditar();
});

document.getElementById('form-editar').addEventListener('submit', function (e) {
    e.preventDefault();
    const id = document.getElementById('edit-id').value;
    const data = new FormData(this);

    fetch(`/admin/productos/editar/${id}`, { method: 'POST', body: data })
        .then(r => r.json())
        .then(d => {
            cerrarModalEditar();
            if (d.ok) {
                Swal.fire({
                    icon: 'success', title: '¡Guardado!', text: d.mensaje,
                    confirmButtonColor: '#e74c3c', timer: 2000, timerProgressBar: true
                }).then(() => location.reload());
            } else {
                Swal.fire({ icon: 'error', title: 'Error al guardar', text: d.mensaje, confirmButtonColor: '#e74c3c' });
            }
        })
        .catch(() => {
            cerrarModalEditar();
            Swal.fire({ icon: 'error', title: 'Error de conexión', text: 'Intenta de nuevo.', confirmButtonColor: '#e74c3c' });
        });
});


// ═══════════════════════════════════════════════════════════════
//  ELIMINAR PRODUCTO
// ═══════════════════════════════════════════════════════════════

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
        data.append('csrf_token', CSRF_E || CSRF_N);

        fetch(`/admin/productos/eliminar/${id}`, { method: 'POST', body: data })
            .then(r => r.json())
            .then(d => {
                if (d.ok) {
                    // Animar y remover tanto la fila como la card
                    ['fila', 'card'].forEach(prefijo => {
                        const el = document.getElementById(`${prefijo}-${id}`);
                        if (el) {
                            el.style.transition = 'opacity 0.4s, transform 0.4s';
                            el.style.opacity = '0';
                            el.style.transform = 'scale(0.95)';
                            setTimeout(() => el.remove(), 420);
                        }
                    });
                    Swal.fire({
                        icon: 'success', title: 'Eliminado', text: d.mensaje,
                        confirmButtonColor: '#e74c3c', timer: 2000, timerProgressBar: true
                    });
                } else {
                    Swal.fire({ icon: 'error', title: 'No se pudo eliminar', text: d.mensaje, confirmButtonColor: '#e74c3c' });
                }
            })
            .catch(() => {
                Swal.fire({ icon: 'error', title: 'Error de conexión', text: 'Intenta de nuevo.', confirmButtonColor: '#e74c3c' });
            });
    });
}


// ═══════════════════════════════════════════════════════════════
//  MODAL — GESTIONAR CATEGORÍAS
// ═══════════════════════════════════════════════════════════════

function abrirModalCategorias() {
    document.getElementById('modal-categorias').style.display = 'flex';
    cargarCategorias();
}

function cerrarModalCategorias() {
    document.getElementById('modal-categorias').style.display = 'none';
}

document.getElementById('modal-categorias').addEventListener('click', function (e) {
    if (e.target === this) cerrarModalCategorias();
});

function cargarCategorias() {
    const lista = document.getElementById('lista-categorias');
    lista.innerHTML = '<div style="text-align:center;padding:20px;color:var(--pikda-gray);"><i class="bi bi-arrow-repeat spin"></i> Cargando...</div>';

    fetch('/admin/categorias')
        .then(r => r.json())
        .then(cats => {
            if (cats.length === 0) {
                lista.innerHTML = '<p style="text-align:center;color:var(--pikda-gray);padding:16px;">No hay categorías todavía.</p>';
                return;
            }
            lista.innerHTML = cats.map(c => `
                <div class="cat-row" id="cat-row-${c.id}">
                    <div>
                        <span class="cat-row-name">${c.nombre}</span>
                        <span class="cat-row-count">${c.total} producto${c.total !== 1 ? 's' : ''}</span>
                    </div>
                    <button class="btn-cat-del" onclick="eliminarCategoria(${c.id}, '${c.nombre}')" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            `).join('');
        })
        .catch(() => {
            lista.innerHTML = '<p style="color:red;padding:16px;">Error al cargar categorías.</p>';
        });
}

// Crear categoría
document.getElementById('form-nueva-cat').addEventListener('submit', function (e) {
    e.preventDefault();
    const data = new FormData(this);

    fetch('/admin/categorias/crear', { method: 'POST', body: data })
        .then(r => r.json())
        .then(d => {
            if (d.ok) {
                document.getElementById('cat-nombre').value = '';
                cargarCategorias();
                mostrarToastRapido('✅ ' + d.mensaje);
            } else {
                Swal.fire({ icon: 'error', title: 'Error', text: d.mensaje, confirmButtonColor: '#e74c3c' });
            }
        })
        .catch(() => {
            Swal.fire({ icon: 'error', title: 'Error de conexión', text: 'Intenta de nuevo.', confirmButtonColor: '#e74c3c' });
        });
});

// Eliminar categoría
function eliminarCategoria(id, nombre) {
    Swal.fire({
        title: '¿Eliminar categoría?',
        html: `Se eliminará <strong>${nombre}</strong>. Solo si no tiene productos.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e74c3c',
        cancelButtonColor: '#6b7280',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then(result => {
        if (!result.isConfirmed) return;

        const data = new FormData();
        data.append('csrf_token', CSRF_C);

        fetch(`/admin/categorias/eliminar/${id}`, { method: 'POST', body: data })
            .then(r => r.json())
            .then(d => {
                if (d.ok) {
                    const row = document.getElementById(`cat-row-${id}`);
                    if (row) {
                        row.style.transition = 'opacity 0.3s';
                        row.style.opacity = '0';
                        setTimeout(() => row.remove(), 320);
                    }
                    mostrarToastRapido('🗑️ ' + d.mensaje);
                } else {
                    Swal.fire({ icon: 'error', title: 'No se pudo eliminar', text: d.mensaje, confirmButtonColor: '#e74c3c' });
                }
            })
            .catch(() => {
                Swal.fire({ icon: 'error', title: 'Error de conexión', text: 'Intenta de nuevo.', confirmButtonColor: '#e74c3c' });
            });
    });
}
