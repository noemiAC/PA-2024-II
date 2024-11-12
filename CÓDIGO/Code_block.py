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
    
    # Convertir la columna FECHA_CORTE en un formato de fecha
    data['FECHA_CORTE'] = pd.to_datetime(data['FECHA_CORTE'], format='%Y%m%d').dt.strftime('%d/%m/%Y')
    
    # Mostrar la tabla original con la fecha formateada
    st.write("Tabla de Datos Original:")
    st.dataframe(data)
    
    # Extraer el año de la columna FECHA_UTC
    data['AÑO'] = data['FECHA_UTC'].astype(str).str[:4]  # Extrae los primeros 4 caracteres como año
    
    # Contar la cantidad de sismos por año
    sismos_por_año = data['AÑO'].value_counts().sort_index()
    
    # Mostrar tabla de cantidad de sismos por año
    st.write("Tabla de cantidad de sismos por año:")
    st.write(sismos_por_año)
    
    # Graficar la cantidad de sismos por año
    fig, ax = plt.subplots()
    sismos_por_año.plot(kind='bar', ax=ax, color="skyblue")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de Sismos")
    ax.set_title("Cantidad de Sismos por Año (1960-2023)")
    st.pyplot(fig)
    
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")


