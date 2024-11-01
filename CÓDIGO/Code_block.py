import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Visualización de Sismos (1960-2023)")

# Ruta del archivo
file_path = "CÓDIGO/Dataset_1960_2023.xlsx"
try:
    # Cargar datos
    data = pd.read_excel(file_path, sheet_name="Catalogo1960_2023")
    
    # Mostrar la tabla original
    st.write("Tabla de Datos Original:")
    st.dataframe(data)  # Muestra la tabla completa al inicio
    
    # Extraer el año de la columna FECHA_UTC
    data['AÑO'] = data['FECHA_UTC'].astype(str).str[:4]  # Extrae los primeros 4 caracteres como año
    
    # Contar la cantidad de sismos por año
    sismos_por_año = data['AÑO'].value_counts().sort_index()
    
    # Mostrar tabla de cantidad de sismos por año
    st.write("Tabla de cantidad de sismos por año:")
    st.write(sismos_por_año)
    
    # Graficar la cantidad de sismos por año con un diseño minimalista
    fig, ax = plt.subplots(figsize=(10, 6))
    sismos_por_año.plot(kind='bar', ax=ax, color="#00A6FB", edgecolor="none")  # Cambia a un color más brillante
    
    # Configuración de estilo minimalista
    ax.set_xlabel("Año", fontsize=10, color="#444444")  # Etiqueta en el eje X con fuente más pequeña
    ax.set_ylabel("Cantidad de Sismos", fontsize=10, color="#444444")  # Etiqueta en el eje Y con fuente más pequeña
    ax.set_title("Cantidad de Sismos por Año (1960-2023)", fontsize=14, color="#222222")  # Título con fuente pequeña y color neutro

    # Cambia el estilo de los ticks y fondo
    ax.tick_params(axis='x', labelsize=8, rotation=90, colors="#666666")  # Tamaño de letra en eje X más pequeño y color gris
    ax.tick_params(axis='y', labelsize=8, colors="#666666")  # Tamaño de letra en eje Y más pequeño y color gris
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#DDDDDD")
    ax.spines['bottom'].set_color("#DDDDDD")
    ax.set_facecolor("white")  # Fondo blanco
    
    # Mostrar la gráfica
    st.pyplot(fig)
    
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
