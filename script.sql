CREATE TABLE MARCA (
    id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE PRODUCTO (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL COLLATE NOCASE UNIQUE,
    descripcion TEXT,
    id_marca INTEGER NOT NULL,
    ubicacion TEXT,
    stock_actual INTEGER NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),

    FOREIGN KEY (id_marca) 
        REFERENCES MARCA(id_marca)
);

CREATE TABLE PROVEEDOR (
    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    contacto TEXT,
    cuit TEXT
);

CREATE TABLE EMPLEADO_DEPOSITO (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    legajo TEXT NOT NULL UNIQUE,
    clave TEXT NOT NULL
);

CREATE TABLE AREA (
    id_area INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    legajo TEXT,
    contacto TEXT
);

CREATE TABLE COMPRA (
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_compra TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    numero_remito TEXT,
    id_proveedor INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,

    FOREIGN KEY (id_proveedor) 
        REFERENCES PROVEEDOR(id_proveedor),

    FOREIGN KEY (id_empleado) 
        REFERENCES EMPLEADO_DEPOSITO(id_empleado)
);

CREATE TABLE DETALLE_COMPRA (
    id_compra INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),

    PRIMARY KEY (id_compra, id_producto),

    FOREIGN KEY (id_compra) 
        REFERENCES COMPRA(id_compra),

    FOREIGN KEY (id_producto) 
        REFERENCES PRODUCTO(id_producto)
);

CREATE TABLE PEDIDO (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_pedido TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    estado TEXT NOT NULL CHECK (estado IN ('Ejecutado')),
    id_area INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,

    FOREIGN KEY (id_area) 
        REFERENCES AREA(id_area),

    FOREIGN KEY (id_empleado) 
        REFERENCES EMPLEADO_DEPOSITO(id_empleado)
);

CREATE TABLE DETALLE_PEDIDO (
    id_pedido INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),

    PRIMARY KEY (id_pedido, id_producto),

    FOREIGN KEY (id_pedido) 
        REFERENCES PEDIDO(id_pedido),

    FOREIGN KEY (id_producto) 
        REFERENCES PRODUCTO(id_producto)
);

CREATE TABLE STOCK_MOVIMIENTO (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    tipo_movimiento TEXT NOT NULL CHECK (tipo_movimiento IN ('INGRESO', 'EGRESO', 'STOCK_INICIAL')),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    id_producto INTEGER NOT NULL,
    id_pedido INTEGER NULL,

    FOREIGN KEY (id_producto) 
        REFERENCES PRODUCTO(id_producto),

    FOREIGN KEY (id_pedido) 
        REFERENCES PEDIDO(id_pedido)
);

-- DATOS DE PRUEBA

INSERT INTO AREA (nombre, legajo, contacto) VALUES ('Ensamble', 'A01', 'ensamble@empresa.com');
INSERT INTO AREA (nombre, legajo, contacto) VALUES ('Mantenimiento', 'A02', 'mantenimiento@empresa.com');
INSERT INTO AREA (nombre, legajo, contacto) VALUES ('Electrónica', 'A03', 'electronica@empresa.com');
INSERT INTO AREA (nombre, legajo, contacto) VALUES ('Calidad', 'A04', 'calidad@empresa.com');

INSERT INTO MARCA (nombre) VALUES ('Genérica');
INSERT INTO MARCA (nombre) VALUES ('Nortec');
INSERT INTO MARCA (nombre) VALUES ('Rodamex');
INSERT INTO MARCA (nombre) VALUES ('Fixmax');
INSERT INTO MARCA (nombre) VALUES ('ElectroPlus');

INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Ferretería Industrial S.A.', 'ventas@ferreteriaindustrial.com', '30-11111111-1');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Electro Cables S.R.L.', 'pedidos@electrocables.com', '30-22222222-2');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Rodamientos del Centro', 'contacto@rodamientoscentro.com', '30-33333333-3');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Tornillos Córdoba S.A.', 'ventas@tornilloscordoba.com', '30-44444444-4');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Metalúrgica Sur S.R.L.', 'info@metalurgicasur.com', '30-55555555-5');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Plásticos del Litoral', 'pedidos@plasticoslitoral.com', '30-66666666-6');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Resortes Argentinos S.A.', 'ventas@resortesarg.com', '30-77777777-7');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Juntas y Sellos S.R.L.', 'contacto@juntassellos.com', '30-88888888-8');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Electrónica Norte', 'pedidos@electronorte.com', '30-99999999-9');
INSERT INTO PROVEEDOR (nombre, contacto, cuit) VALUES ('Distribuidora Técnica S.A.', 'ventas@distribuidoratecnica.com', '30-10101010-1');

INSERT INTO EMPLEADO_DEPOSITO (nombre, legajo, clave) VALUES ('administrador', 'admin', '29a24d5030def1ff767c47453b314763$baa13b57e72a20c26bd205a2d5cd022e01aac1e3bfae86589a6dfc12aa092bb2');
INSERT INTO EMPLEADO_DEPOSITO (nombre, legajo, clave) VALUES ('Carlos Gómez', 'E001', 'c4104a76ff63d9d2ef7af57f75faa34c$4d00d1fa7fd0d3e72d5892716a46f3cb4bcdd24e06f116e2b608eb8444d51384');
INSERT INTO EMPLEADO_DEPOSITO (nombre, legajo, clave) VALUES ('Lucía Fernández', 'E002', '27499e8936f1718d307a31ab80a85e9a$dca1bb259b217d61860a86166f5eb50e3fd5bf9c480e5ef224d7bdf60ab923b1');
INSERT INTO EMPLEADO_DEPOSITO (nombre, legajo, clave) VALUES ('Martín Ríos', 'E003', 'e927f98915164d8e57e3e18ac30c335c$83125b5c6f5f39a05e68ff55472cd380d715f8a62895033c47da907d9f8148b9');
INSERT INTO EMPLEADO_DEPOSITO (nombre, legajo, clave) VALUES ('Sofía Álvarez', 'E004', '5ea7af9857496bb43291b10c9e98430a$3321bc49147cfe8c14eb69686ec1a2a8f36a6ea3ecf5723ae30ab62008c6b940');

-- PRODUCTOS (el stock_actual ya incluye los ingresos y egresos cargados mas abajo)
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (1, 'Tornillo M6', 'Tornillo cabeza hexagonal M6 x 20 mm', 4, 'A-01', 222);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (2, 'Tuerca M6', 'Tuerca hexagonal M6', 4, 'A-02', 323);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (3, 'Placa Base A1', 'Placa base de aluminio para ensamble', 2, 'B-01', 95);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (4, 'Soporte Motor', 'Soporte de acero para motor', 2, 'B-02', 22);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (5, 'Espina M8', 'Espina de acero M8', 4, 'A-03', 60);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (6, 'Resorte', 'Resorte de compresión', 1, 'C-01', 132);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (7, 'Oring', 'Anillo de goma (o-ring)', 1, 'C-02', 128);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (8, 'Cables 1,5mm', 'Cable unipolar de 1,5 mm', 5, 'D-01', 103);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (9, 'Cable 3mm', 'Cable unipolar de 3 mm', 5, 'D-02', 25);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (10, 'Reguladores de caudal', 'Regulador de caudal neumático', 2, 'B-03', 115);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (11, 'Rodamiento 6204', 'Rodamiento rígido de bolas 6204', 3, 'E-01', 180);
INSERT INTO PRODUCTO (id_producto, nombre, descripcion, id_marca, ubicacion, stock_actual) VALUES (12, 'Junta de goma', 'Junta de goma para tapa', 1, 'C-03', 62);

-- COMPRAS (ingreso de mercaderia)
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (1, '2026-09-04 14:12:00', 'R-0001-00004507', 9, 2);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (2, '2026-09-08 09:16:00', 'R-0001-00004514', 1, 5);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (3, '2026-09-11 15:12:00', 'R-0001-00004521', 10, 1);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (4, '2026-09-16 14:55:00', 'R-0001-00004528', 9, 4);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (5, '2026-09-18 13:05:00', 'R-0001-00004535', 6, 3);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (6, '2026-09-23 08:17:00', 'R-0001-00004542', 1, 4);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (7, '2026-09-28 16:05:00', 'R-0001-00004549', 8, 4);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (8, '2026-10-01 15:03:00', 'R-0001-00004556', 3, 2);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (9, '2026-10-06 15:38:00', 'R-0001-00004563', 7, 4);
INSERT INTO COMPRA (id_compra, fecha_compra, numero_remito, id_proveedor, id_empleado) VALUES (10, '2026-10-08 08:07:00', 'R-0001-00004570', 9, 1);

-- DETALLE DE COMPRAS
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (1, 1, 20);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (1, 2, 50);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (1, 9, 10);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (2, 11, 60);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (2, 10, 10);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (2, 1, 30);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (3, 10, 50);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (3, 11, 20);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (3, 4, 20);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (4, 2, 40);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (5, 7, 20);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (5, 1, 50);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (6, 10, 40);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (6, 11, 60);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (6, 8, 50);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (7, 7, 20);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (7, 8, 25);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (8, 4, 20);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (8, 3, 25);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (9, 10, 10);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (9, 6, 100);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (9, 3, 60);
INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad) VALUES (10, 1, 25);

-- PEDIDOS
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (1, '2026-09-07 11:15:00', 'Ejecutado', 4, 1);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (2, '2026-09-10 16:43:00', 'Ejecutado', 3, 5);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (3, '2026-09-14 11:50:00', 'Ejecutado', 3, 3);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (4, '2026-09-17 10:29:00', 'Ejecutado', 4, 2);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (5, '2026-09-21 15:20:00', 'Ejecutado', 1, 1);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (6, '2026-09-24 14:13:00', 'Ejecutado', 2, 3);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (7, '2026-09-30 16:57:00', 'Ejecutado', 3, 4);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (8, '2026-10-05 10:13:00', 'Ejecutado', 1, 2);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (9, '2026-10-07 16:42:00', 'Ejecutado', 2, 1);
INSERT INTO PEDIDO (id_pedido, fecha_pedido, estado, id_area, id_empleado) VALUES (10, '2026-10-09 10:30:00', 'Ejecutado', 4, 2);

-- DETALLE DE PEDIDOS
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (1, 2, 2);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (1, 4, 8);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (2, 9, 2);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (3, 9, 8);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (3, 7, 10);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (3, 6, 8);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (4, 10, 2);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (4, 2, 10);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (5, 2, 5);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (5, 12, 8);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (6, 8, 2);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (7, 7, 20);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (8, 10, 5);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (8, 3, 5);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (9, 7, 2);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (9, 1, 3);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (9, 4, 8);
INSERT INTO DETALLE_PEDIDO (id_pedido, id_producto, cantidad) VALUES (10, 4, 10);

-- MOVIMIENTOS DE STOCK (stock inicial, ingresos y egresos)
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 100, 1, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 250, 2, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 15, 3, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 8, 4, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 60, 5, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 40, 6, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 120, 7, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 30, 8, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 25, 9, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 12, 10, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 40, 11, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-01 08:00:00', 'STOCK_INICIAL', 70, 12, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-04 14:12:00', 'INGRESO', 20, 1, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-04 14:12:00', 'INGRESO', 50, 2, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-04 14:12:00', 'INGRESO', 10, 9, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-07 11:15:00', 'EGRESO', 2, 2, 1);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-07 11:15:00', 'EGRESO', 8, 4, 1);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-08 09:16:00', 'INGRESO', 60, 11, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-08 09:16:00', 'INGRESO', 10, 10, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-08 09:16:00', 'INGRESO', 30, 1, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-10 16:43:00', 'EGRESO', 2, 9, 2);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-11 15:12:00', 'INGRESO', 50, 10, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-11 15:12:00', 'INGRESO', 20, 11, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-11 15:12:00', 'INGRESO', 20, 4, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-14 11:50:00', 'EGRESO', 8, 9, 3);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-14 11:50:00', 'EGRESO', 10, 7, 3);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-14 11:50:00', 'EGRESO', 8, 6, 3);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-16 14:55:00', 'INGRESO', 40, 2, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-17 10:29:00', 'EGRESO', 2, 10, 4);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-17 10:29:00', 'EGRESO', 10, 2, 4);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-18 13:05:00', 'INGRESO', 20, 7, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-18 13:05:00', 'INGRESO', 50, 1, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-21 15:20:00', 'EGRESO', 5, 2, 5);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-21 15:20:00', 'EGRESO', 8, 12, 5);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-23 08:17:00', 'INGRESO', 40, 10, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-23 08:17:00', 'INGRESO', 60, 11, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-23 08:17:00', 'INGRESO', 50, 8, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-24 14:13:00', 'EGRESO', 2, 8, 6);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-28 16:05:00', 'INGRESO', 20, 7, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-28 16:05:00', 'INGRESO', 25, 8, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-09-30 16:57:00', 'EGRESO', 20, 7, 7);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-01 15:03:00', 'INGRESO', 20, 4, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-01 15:03:00', 'INGRESO', 25, 3, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-05 10:13:00', 'EGRESO', 5, 10, 8);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-05 10:13:00', 'EGRESO', 5, 3, 8);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-06 15:38:00', 'INGRESO', 10, 10, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-06 15:38:00', 'INGRESO', 100, 6, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-06 15:38:00', 'INGRESO', 60, 3, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-07 16:42:00', 'EGRESO', 2, 7, 9);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-07 16:42:00', 'EGRESO', 3, 1, 9);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-07 16:42:00', 'EGRESO', 8, 4, 9);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-08 08:07:00', 'INGRESO', 25, 1, NULL);
INSERT INTO STOCK_MOVIMIENTO (fecha, tipo_movimiento, cantidad, id_producto, id_pedido) VALUES ('2026-10-09 10:30:00', 'EGRESO', 10, 4, 10);