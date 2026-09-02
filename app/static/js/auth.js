/* ══════════════════════════════════════════════════════════
   auth.js  —  Scripts del módulo de autenticación
   ══════════════════════════════════════════════════════════ */

/**
 * Alterna visibilidad de la contraseña.
 * Se usa en login_admin.html y login_empleado.html.
 */
function togglePassword() {
    const input = document.getElementById('password');
    const icon  = document.getElementById('eye-icon');

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('bi-eye-slash', 'bi-eye');
    }
}