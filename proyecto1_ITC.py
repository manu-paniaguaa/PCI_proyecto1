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
        
    

Se tuvieron que hacer cambios debido a incompatibilidades entre las librerias
"""


########################################################################
## para ejecutar insertar en terminal: streamlit run Proyecto1_ITC.py ##
########################################################################

"""Documentaciones de librerias:
    - pandas: https://pandas.pydata.org/docs/
    - streamlit: https://docs.streamlit.io/
    - io: https://docs.python.org/3/library/io.html
    - plotly: https://plotly.com/python/
"""
import pandas as pd 
import streamlit as st
from io import BytesIO
import plotly.express as px

MARGEN_VERDE = 25
MARGEN_AMARILLO = 15
MAX_INTENTOS = 3
COLORES = ['green', 'yellow', 'red']
COLUMNAS_NECESARIAS = ["Producto", "Precio Venta(sin IVA)", "Costo(sin IVA)"]


def configurar_pagina():
    """Configura el título y el layout de la página de Streamlit."""
    st.set_page_config(page_title="Proyecto ITC", layout='wide')
    st.title("Gráfico de Margen de Productos")


def calcular_margen(datos):
    """
    Calcula el margen porcentual de cada producto.
    
    El margen se calcula como: (Precio - Costo) / Precio * 100
    """
    datos["Margen %"] = ((datos["Precio Venta(sin IVA)"] 
                          - datos["Costo(sin IVA)"]) 
                         / datos["Precio Venta(sin IVA)"])
    datos["Margen %"] = datos["Margen %"] * 100.0
    datos["Margen %"] = datos["Margen %"].round(1)
    return datos


def formato_condicional(valor):
    """
    Aplica formato condicional según el valor del margen.
    
    Verde: >= 25%
    Amarillo: >= 15%
    Rojo: < 15%
    """
    
    if valor >= MARGEN_VERDE:
        color = COLORES[0]
    elif valor >= MARGEN_AMARILLO:
        color = COLORES[1]
    else:
        color = COLORES[2]
    
    return f'background-color: {color}'


def crear_grafico(datos):
    """Crea un gráfico de barras con la información de productos."""
    grafico = px.bar(
        datos,
        x="Producto",
        y=["Precio Venta(sin IVA)", "Costo(sin IVA)", "Margen %"]
    )
    return grafico


def mostrar_datos_y_grafico(datos):
    """Muestra la tabla de datos y el gráfico en la interfaz."""
    datos_con_margen = calcular_margen(datos)
    
    st.dataframe(
        datos_con_margen.head(10).style.applymap(
            formato_condicional,
            subset=["Margen %"]
        )
    )
    
    grafico = crear_grafico(datos_con_margen)
    st.plotly_chart(grafico, use_container_width=True)


def validar_columnas(datos):
    """Verifica si el DataFrame contiene las columnas necesarias."""
    return all(columna in datos.columns for columna in COLUMNAS_NECESARIAS)


def procesar_archivo(archivo_subido):
    """
    Procesa el archivo Excel subido y genera los gráficos.
    
    Permite hasta 3 intentos si el archivo no contiene las columnas correctas.
    """
    if archivo_subido is None:
        print("No se subió ningún archivo.")
        return
    
    try:
        intentos = 0
        archivo_valido = False
        
        while intentos < MAX_INTENTOS and not archivo_valido:
            datos = pd.read_excel(archivo_subido)
            
            if validar_columnas(datos):
                archivo_valido = True
            else:
                intentos += 1
                st.warning(
                    f"Archivo no válido. Intento {intentos} de "
                    f"{MAX_INTENTOS}. Verifica las columnas."
                )
                
                if intentos == MAX_INTENTOS:
                    st.error(
                        "Número máximo de intentos alcanzado. "
                        "Verifica tu archivo."
                    )
                    return
        
        print(datos)
        mostrar_datos_y_grafico(datos)
        
    except Exception as error:
        st.error(f"Ocurrió un error: {error}")


def main():
    """Función principal que ejecuta la aplicación."""
    configurar_pagina()
    
    archivo_subido = st.file_uploader(
        "Selecciona un archivo Excel",
        type=["xlsx", "xls"]
    )
    
    procesar_archivo(archivo_subido)

main()