CREATE DATABASE SistemaControlStock;

USE SistemaControlStock;


CREATE TABLE EMPLEADO (
    id_empleado INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE
);


CREATE TABLE MARCA (
    id_marca INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE PRODUCTO (
    id_producto INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    id_marca INT NOT NULL,
    ubicacion VARCHAR(100),
    stock_actual INT NOT NULL DEFAULT 0,

    FOREIGN KEY (id_marca)
        REFERENCES MARCA(id_marca),

    CHECK (stock_actual >= 0)
);


CREATE TABLE PROVEEDOR (
    id_proveedor INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(30),
    email VARCHAR(100),
    direccion VARCHAR(150)
);


CREATE TABLE PEDIDO (
    id_pedido INT IDENTITY(1,1) PRIMARY KEY,
    fecha_pedido DATETIME NOT NULL DEFAULT GETDATE(),
    id_empleado INT NOT NULL,

    FOREIGN KEY (id_empleado)
        REFERENCES EMPLEADO(id_empleado)
);


CREATE TABLE DETALLE_PEDIDO (
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,

    PRIMARY KEY (id_pedido, id_producto),

    FOREIGN KEY (id_pedido)
        REFERENCES PEDIDO(id_pedido),

    FOREIGN KEY (id_producto)
        REFERENCES PRODUCTO(id_producto),

    CHECK (cantidad > 0)
);


CREATE TABLE COMPRA (
    id_compra INT IDENTITY(1,1) PRIMARY KEY,
    fecha_compra DATETIME NOT NULL DEFAULT GETDATE(),
    id_proveedor INT NOT NULL,
    numero_remito VARCHAR(50),

    FOREIGN KEY (id_proveedor)
        REFERENCES PROVEEDOR(id_proveedor)
);


CREATE TABLE DETALLE_COMPRA (
    id_compra INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,

    PRIMARY KEY (id_compra, id_producto),

    FOREIGN KEY (id_compra)
        REFERENCES COMPRA(id_compra),

    FOREIGN KEY (id_producto)
        REFERENCES PRODUCTO(id_producto),

    CHECK (cantidad > 0)
);