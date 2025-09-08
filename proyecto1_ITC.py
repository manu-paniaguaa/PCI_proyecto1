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


import pandas as pd #Documentation: https://pandas.pydata.org/docs/
import streamlit as st #Documentation: https://docs.streamlit.io/
from io import BytesIO # Documentation: https://docs.python.org/3/library/io.html
import plotly.express as px #Documentation: https://plotly.com/graphing-libraries/

st.set_page_config(page_title="Proyecto ITC", layout='wide') #Se crea el sitio web con titulo de pestaña y el formato de pantalla completa
st.title("Gráfico de Margen de Productos") #Titulo de la página


uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx", "xls"]) #Se encarga de solicitar al usuario el archivo excel, previamente se utilizaba Tkinter pero por problemas de compatibilidad se recurrió al uso completo de streamlit para el upload 
#también asegura que solo se suban archivos xlsx o xls. 

def conditional_format(val): #esto es el formato condicional para mostrar al usuario si los margenes estan bien 
    if val >= 25:
        color = 'green' #si el margen es mayor a 25% se pinta verde
    elif val >= 15:
        color = 'yellow' #si el margen es mayor a 20% se pinta amarillo
    else:
        color = 'red' #si el margen es menor se pinta rojo 
    return f'background-color: {color}' #nos devuelve la funcion necesaria para ejecutar el codigo en la configuracion del datafframe

def calcular_margenes():
    if uploaded_file is not None: #solo corre el código si se subio un archivo
        try:
            data = pd.read_excel(uploaded_file) #lee con pandas el archivo excel y lo convierte en un archivo de data manejable 
            data["Margen %"] = (data["Precio Venta(sin IVA)"] - data["Costo(sin IVA)"]) / data["Precio Venta(sin IVA)"] #agrega la columna margen y hace el calculo
            data["Margen %"] = data["Margen %"] * 100 #multiplica el resultado por 100 para que sea el porcentaje
            data["Margen %"] = data["Margen %"].round(1) #redondea a 1 cifra
            output = BytesIO() #crea un archivo en blanco que no se guarda en la memoria para posteriormente ahi guardar el libro de excel modificado 
            with pd.ExcelWriter(output, engine='openpyxl') as writer: #nos permite sobreescribir el archivo que subimos
                data.to_excel(writer, index=False) #importa la informacion del dataframe al excel para graficar y mostrar
            output.seek(0) #reestablece el inicio del archivo en el inicio el libro para leer toda la informacion, de otro modo, intentaria leer el archivo en donde lo dejo la escritura que es el final de las filas, y a partir de ahi no hay nada, por ello se hace esto.
            st.dataframe(data.head(10).style.applymap(conditional_format, subset=["Margen %"])) #escribe una tabla para visualizar la información solo muestra las primeras 10 filas, adicional establece formato condicional a las celdas de margen.
            grafico = px.bar( #grafico de barras integrado en streamlit por plotly 
                data, #muestra la informacuon de data
                x="Producto", #en el eje x muestra el producto
                y=[f"Precio Venta(sin IVA)", "Costo(sin IVA)", "Margen %"], #eje y muestra la info del producto apilada
            )
            st.plotly_chart(grafico, use_container_width=True) #inserta el grafico en el sitio web
        except Exception as error: #si hay un error muestra el error dentro de streamlit
            st.error(f"Ocurrió un error: {error}")

calcular_margenes()
