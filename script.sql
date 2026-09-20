CREATE TABLE MARCA (
    id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE PRODUCTO (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
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
    legajo TEXT NOT NULL UNIQUE
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
    estado TEXT NOT NULL,
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
    tipo_movimiento TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    id_pedido INTEGER NULL,

    FOREIGN KEY (id_producto) 
        REFERENCES PRODUCTO(id_producto),

    FOREIGN KEY (id_pedido) 
        REFERENCES PEDIDO(id_pedido)
);