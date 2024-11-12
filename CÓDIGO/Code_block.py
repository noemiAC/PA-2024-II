import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# Título de la aplicación
st.title("Visualización de Sismos (1960-2023)")

# Ruta del archivo
file_path = "CÓDIGO/Dataset_1960_2023.xlsx"
try:
    # Cargar datos
    data = pd.read_excel(file_path, sheet_name="Catalogo1960_2023")
    
    # Convertir FECHA_UTC a formato de fecha (datetime)
    data['FECHA_UTC'] = pd.to_datetime(data['FECHA_UTC'].astype(str), format='%Y%m%d')
    data['FECHA_UTC'] = data['FECHA_UTC'].dt.strftime('%d/%m/%Y')
    
    # Mostrar la tabla de datos original
    st.write("Tabla de Datos Original con FECHA_UTC formateada:")
    st.dataframe(data)
    
    # Verificación de columnas de latitud y longitud para el mapa
    if 'LATITUD' in data.columns and 'LONGITUD' in data.columns:
        # Convertir a numérico para asegurarse de que no haya errores
        data['LATITUD'] = pd.to_numeric(data['LATITUD'], errors='coerce')
        data['LONGITUD'] = pd.to_numeric(data['LONGITUD'], errors='coerce')
        
        # Filtrar filas con valores válidos de latitud y longitud
        data = data.dropna(subset=['LATITUD', 'LONGITUD'])
        
        # Crear el mapa centrado en una ubicación promedio de los sismos
        m = folium.Map(location=[data['LATITUD'].mean(), data['LONGITUD'].mean()], zoom_start=5)

        # Añadir marcadores al mapa para cada sismo
        for _, row in data.iterrows():
            folium.Marker(
                location=[row['LATITUD'], row['LONGITUD']],
                popup=f"Fecha: {row['FECHA_UTC']}<br>Magnitud: {row['MAGNITUD']}",
                tooltip=row['FECHA_UTC']
            ).add_to(m)

        # Mostrar el mapa en Streamlit, debajo de la tabla de datos
        st.write("Mapa de sismos:")
        st_folium(m, width=700, height=500)
    else:
        st.error("El archivo no contiene columnas de LATITUD y LONGITUD necesarias para el mapa.")
    
    # Extraer el año de la columna FECHA_UTC (ya en string)
    data['AÑO'] = data['FECHA_UTC'].str[-4:]  # Extrae el año
    
    # Contar la cantidad de sismos por año
    sismos_por_año = data['AÑO'].value_counts().sort_index()
    
    # Mostrar tabla de cantidad de sismos por año
    st.write("Tabla de cantidad de sismos por año:")
    st.write(sismos_por_año)
    
    # Crear un selectbox para elegir el tipo de gráfico
    grafico_tipo = st.selectbox("Selecciona el tipo de gráfico", ("Gráfico de Barras", "Histograma", "Gráfico de Líneas"))
    
    # Configuración de diseño de gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    # Condicional para mostrar el gráfico seleccionado
    if grafico_tipo == "Gráfico de Barras":
        sismos_por_año.plot(kind='bar', ax=ax, color="#00A6FB", edgecolor="none")
        ax.set_title("Cantidad de Sismos por Año (1960-2023) - Gráfico de Barras")
    elif grafico_tipo == "Histograma":
        sismos_por_año.plot(kind='hist', bins=30, ax=ax, color="#FF6B6B", edgecolor="none")
        ax.set_title("Cantidad de Sismos por Año (1960-2023) - Histograma")
    elif grafico_tipo == "Gráfico de Líneas":
        sismos_por_año.plot(kind='line', ax=ax, color="#1FAB89", linewidth=2)
        ax.set_title("Cantidad de Sismos por Año (1960-2023) - Gráfico de Líneas")
    
    # Configuración minimalista de etiquetas
    ax.set_xlabel("Año", fontsize=10, color="#444444")
    ax.set_ylabel("Cantidad de Sismos", fontsize=10, color="#444444")
    ax.tick_params(axis='x', labelsize=8, rotation=90, colors="#666666")
    ax.tick_params(axis='y', labelsize=8, colors="#666666")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#DDDDDD")
    ax.spines['bottom'].set_color("#DDDDDD")
    ax.set_facecolor("white")
    
    # Mostrar el gráfico
    st.pyplot(fig)
    
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")

