# Sistema de control de stock para empresa de máquinas de ensamble.

## Descripción 

Sistema de control de stock interno diseñado para empresa de máquinas de ensamble. Permite gestionar inventarios, registrar entradas y salidas de componentes críticos, y asegurar la trazabilidad de piezas utilizadas en cada orden de montaje.

Incluye un Diagrama Entidad-Relación (DER) que modela componentes clave como Productos, Stock, Movimientos, Compras, Pedidos, Proveedores, Áreas y Empleados de depósito.

## Organización

El equipo de 5 integrantes (Agustín Rosa, Ian Montoya, Jessica Pereyra, Matias Petenatti y Jonathan Piedrabuena) tiene roles distribuidos de forma clara en áreas de coordinación, modelado de datos, diseño de interfaz, acceso a datos, validaciones y documentación.

## Características principales  

- **Control de Inventario de Componentes**: Registro detallado de entradas, salidas y stock actual de piezas mecánicas, electrónicas y tornillería. 
- **Alertas de Stock Crítico**: Avisos automáticos cuando los componentes esenciales se encuentran por debajo del nivel mínimo de seguridad. 
- **Gestión de Proveedores**: Registro de la procedencia de los insumos para facilitar el control de calidad y reposición. 
- **Consultas y Reportes**: Visualización rápida del estado actual del almacén y el historial de movimientos.


## Tecnologías Utilizadas

La aplicación se programa en Python, utiliza bases de datos con sentencias SQL y su interfaz gráfica se diseña mediante la librería Tkinter, contemplando pantallas para inicio de sesión, consulta de stock, ejecución de pedidos e ingreso de mercadería.
