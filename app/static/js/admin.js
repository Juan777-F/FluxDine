/* ══════════════════════════════════════════════════════════
   admin.js  —  Panel Administrador · FluxDine
   ══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

    // ── Gráfico de barras semanal (estático por ahora) ─────
    const datos = {
        dias: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
        ventas: [180000, 240000, 210000, 270000, 310000, 390000, 150000],
        meta: [250000, 250000, 250000, 250000, 250000, 250000, 250000],
    };

    const container = document.getElementById('chart-bars');
    const labels = document.getElementById('chart-labels');

    if (container && labels) {
        const maxVal = Math.max(...datos.ventas, ...datos.meta);

        datos.dias.forEach((dia, i) => {
            const altVenta = (datos.ventas[i] / maxVal * 100).toFixed(1);
            const altMeta = (datos.meta[i] / maxVal * 100).toFixed(1);

            // Barras
            const group = document.createElement('div');
            group.style.cssText = 'flex:1;display:flex;align-items:flex-end;gap:3px;height:100%;';

            const barVenta = document.createElement('div');
            barVenta.className = 'chart-bar venta';
            barVenta.style.cssText = `flex:1;height:${altVenta}%;`;
            barVenta.title = `Ventas: $${datos.ventas[i].toLocaleString('es-CO')}`;

            const barMeta = document.createElement('div');
            barMeta.className = 'chart-bar meta';
            barMeta.style.cssText = `flex:1;height:${altMeta}%;`;
            barMeta.title = `Meta: $${datos.meta[i].toLocaleString('es-CO')}`;

            group.appendChild(barVenta);
            group.appendChild(barMeta);
            container.appendChild(group);

            // Etiquetas
            const label = document.createElement('div');
            label.style.cssText = 'flex:1;text-align:center;font-size:0.72rem;color:var(--pikda-gray);';
            label.textContent = dia;
            labels.appendChild(label);
        });
    }

    // ── Búsqueda en topbar (placeholder funcional) ─────────
    const searchInput = document.querySelector('.topbar-search input');
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const q = searchInput.value.trim();
                if (q) window.location.href = `/admin/buscar?q=${encodeURIComponent(q)}`;
            }
        });
    }

    // ── Marcar nav-item activo según URL actual ─────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath.startsWith(href) && href !== '/') {
            item.classList.add('active');
        } else if (href === '/admin' && currentPath === '/admin') {
            item.classList.add('active');
        }
    });

});