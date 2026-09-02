/* ══════════════════════════════════════════════════════════
   pikda.js  —  Scripts globales del sistema La Pikda
   ══════════════════════════════════════════════════════════ */

/* ── Auto-cerrar alertas flash tras 4 segundos ────────────── */
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelectorAll('.flash-container .alert').forEach(el => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
            bsAlert.close();
        });
    }, 4000);
});