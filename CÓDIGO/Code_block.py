import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Visualización de Datos Sísmicos (1960-2023)")

# Cargar el archivo de Excel
file_path = "CÓDIGO/Dataset_1960_2023.xlsx"
try:
    data = pd.read_excel(file_path, sheet_name="Catalogo1960_2023")
    st.write("Datos cargados exitosamente.")
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    data = None

# Mostrar los datos si se cargaron correctamente
if data is not None:
    st.write("Vista previa de los datos:")
    st.dataframe(data)

    # Opcional: Mostrar estadísticas descriptivas
    st.write("Estadísticas descriptivas:")
    st.write(data.describe())
