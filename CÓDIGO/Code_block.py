import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo Excel
df = pd.read_excel("CÓDIGO/Dataset_1960_2023.xlsx")

# Convertir FECHA_CORTE a fecha en formato "día/mes/año"
df['FECHA_CORTE'] = pd.to_datetime(df['FECHA_CORTE'], format='%Y%m%d').dt.strftime('%d/%m/%Y')

# Convertir FECHA_UTC a fecha en formato "día/mes/año"
df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y%m%d').dt.strftime('%d/%m/%Y')

# Mostrar tabla de datos original
st.markdown("### Tabla de Datos Original:")
st.dataframe(df)

# Contar la cantidad de sismos por año
df['AÑO'] = pd.to_datetime(df['FECHA_UTC'], format='%d/%m/%Y').dt.year  # Extraer el año de FECHA_UTC
sismos_por_año = df['AÑO'].value_counts().sort_index()

# Graficar la cantidad de sismos por año
fig, ax = plt.subplots()
sismos_por_año.plot(kind='bar', ax=ax)
ax.set_xlabel("Año")
ax.set_ylabel("Cantidad de Sismos")
ax.set_title("Cantidad de Sismos por Año")
st.pyplot(fig)


