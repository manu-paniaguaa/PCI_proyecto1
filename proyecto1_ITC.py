# Aqui se irá actualizando el proyecto para su total funcionalidad a lo largo del curso de ITC

"""
ENTRADAS:
    1. Solicitar al usuario el formato excel preestablecido con el nombre/clave de los productos, costo y precio.

PROCESO:
    1. Ingresar el Excel_productos
    2. Utilizar pandas para agregar una tercera columna después de (nombre/clave, precio_venta, costo)
    3. En la cuarta columna creada por pandas establecer una fórmula de Margen = (precio_venta - costo)/precio_venta
        3.1 Formato en porcentaje para la columna 4
        3.2 Usar filtro para organizar las columnas por margen de mayor a menor
    4. Crear una quinta columna con formula promedio_margen = (SUM(Margen)/COUNT(Margen))
    5. Importar informacion como CSV a streamlit
    6. Crear variable diferencia = ((margen - promedio margen)/promedio margen)*100
    7. Crear visualizacion de gráfico de barras con reglas:
        7.1 While diferencia >= 5 pintar en verde la columna del producto por que tiene margen sobresaliente
        7.2 While diferencia <= -5 pintar en rojo la columna del producto por que tiene margen subsaliente
        7.3 SINO pintar en azul la columna del producto por que el margen esta dentro del rango

SALIDAS: 
    Gráfico de barras dinámico que muestre tus porductos junto con una linea del margen promedio y cambia el color de los productos sobre o sub 
    salientes dentro de tu inventario ordenados de mayor a menor.
        
"""