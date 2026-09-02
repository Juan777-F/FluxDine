/* ══════════════════════════════════════════════════════════
   empleado.js  —  Panel Empleado · La Pikda
   ══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

    // ── Reloj del turno en tiempo real ──────────────────────
    const clockEl = document.getElementById('turno-hora');
    if (clockEl) {
        const actualizarHora = () => {
            const ahora = new Date();
            clockEl.textContent = ahora.toLocaleTimeString('es-CO', {
                hour: '2-digit', minute: '2-digit'
            });
        };
        actualizarHora();
        setInterval(actualizarHora, 60000);
    }

    // ── Marcar nav-item activo según URL ────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath.startsWith(href) && href !== '/') {
            item.classList.add('active');
        } else if (href === '/empleado' && currentPath === '/empleado') {
            item.classList.add('active');
        }
    });

    // ── Confirmar cierre de sesión ──────────────────────────
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            if (!confirm('¿Seguro que quieres cerrar tu turno?')) {
                e.preventDefault();
            }
        });
    }

});