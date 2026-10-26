-- ╔══════════════════════════════════════════════════════════╗
-- ║  LA PIKDA — Migración: campos nuevos en 'productos'      ║
-- ║  Ejecuta este script en MySQL Workbench o phpMyAdmin      ║
-- ╚══════════════════════════════════════════════════════════╝

USE la_pikda_db;

-- Agrega campo 'destacado' (producto estrella del menú)
ALTER TABLE productos
    ADD COLUMN destacado TINYINT(1) NOT NULL DEFAULT 0
    AFTER estado;

-- Agrega campo 'imagen_url' (URL de imagen del producto)
ALTER TABLE productos
    ADD COLUMN imagen_url VARCHAR(255) NULL DEFAULT NULL
    AFTER destacado;

-- Verifica los cambios
DESCRIBE productos;
