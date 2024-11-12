# PRIMER AVANCE CÓDIGO  - Code_block                                                                                                                                                              import streamlit as st
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
    
    data['AÑO'] = data['FECHA_UTC'].astype(str).str[:4]  # Extrae los primeros 4 caracteres como año

    # Extraer el año de la columna FECHA_UTC
    
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

