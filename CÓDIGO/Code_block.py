import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Visualización de Sismos (1960-2023)")

# Ruta del archivo
file_path = "CÓDIGO/Dataset_1960_2023.xlsx"
try:
    # Cargar datos
    data = pd.read_excel(file_path)

    # Convertir FECHA_UTC al formato de fecha (YYYYMMDD -> YYYY-MM-DD) sin la hora
    data['FECHA_UTC'] = pd.to_datetime(data['FECHA_UTC'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')

    # Convertir FECHA_CORTE al formato de fecha (YYYYMMDD -> YYYY-MM-DD) sin la hora
    data['FECHA_CORTE'] = pd.to_datetime(data['FECHA_CORTE'], format='%Y%d%m', errors='coerce').dt.strftime('%Y-%d-%m')

    # Convertir HORA_UTC al formato de hora (horas, minutos, segundos)
    data['HORA_UTC'] = pd.to_datetime(data['HORA_UTC'], errors='coerce', format='%H%M%S').dt.time

    
    # Mostrar la tabla original
    st.write("Tabla de Datos Original:")
    st.dataframe(data)  # Muestra la tabla completa al inicio
    
    # Verificar si la columna 'PROFUNDIDAD' existe y filtrar por profundidad
    if 'PROFUNDIDAD' in data.columns:
        # Filtro de profundidad con un slider
        profundidad_min = int(data['PROFUNDIDAD'].min())
        profundidad_max = int(data['PROFUNDIDAD'].max())
        
        profundidad_filtrada = st.slider(
            "Selecciona el rango de profundidad (km)",
            min_value=profundidad_min, max_value=profundidad_max,
            value=(profundidad_min, profundidad_max),
            step=1
        )
        
        # Filtrar los sismos por el rango de profundidad
        data = data[(data['PROFUNDIDAD'] >= profundidad_filtrada[0]) & 
                    (data['PROFUNDIDAD'] <= profundidad_filtrada[1])]
        
        # Mostrar los datos filtrados por profundidad
        st.write(f"Datos filtrados por profundidad entre {profundidad_filtrada[0]} y {profundidad_filtrada[1]} km:")
        st.dataframe(data)
    else:
        st.error("La columna 'PROFUNDIDAD' no se encuentra en el archivo.")
    
    # Verificar si la columna 'MAGNITUD' existe y filtrar por magnitud
    if 'MAGNITUD' in data.columns:
        # Filtro de magnitud con un slider
        magnitud_min = float(data['MAGNITUD'].min())
        magnitud_max = float(data['MAGNITUD'].max())
        
        magnitud_filtrada = st.slider(
            "Selecciona el rango de magnitud",
            min_value=magnitud_min, max_value=magnitud_max,
            value=(magnitud_min, magnitud_max),
            step=0.1
        )
        
        # Filtrar los sismos por el rango de magnitud
        data = data[(data['MAGNITUD'] >= magnitud_filtrada[0]) & 
                    (data['MAGNITUD'] <= magnitud_filtrada[1])]
        
        # Mostrar los datos filtrados por magnitud
        st.write(f"Datos filtrados por magnitud entre {magnitud_filtrada[0]} y {magnitud_filtrada[1]}:")
        st.dataframe(data)
    else:
        st.error("La columna 'MAGNITUD' no se encuentra en el archivo.")
    
    # Verificar si la columna 'LATITUD' existe y filtrar por latitud
    if 'LATITUD' in data.columns:
        data['LATITUD'] = pd.to_numeric(data['LATITUD'], errors='coerce')
        # Filtro de latitud para Perú (-18 a 0)
        latitud_min = -18.0
        latitud_max = 0.0
        
        latitud_filtrada = st.slider(
            "Selecciona el rango de latitud en Perú",
            min_value=latitud_min, max_value=latitud_max,
            value=(latitud_min, latitud_max),
            step=0.1
        )
        
        # Filtrar los sismos por el rango de latitud
        data = data[(data['LATITUD'] >= latitud_filtrada[0]) & 
                    (data['LATITUD'] <= latitud_filtrada[1])]
        
        # Mostrar los datos filtrados por latitud
        st.write(f"Datos filtrados por latitud entre {latitud_filtrada[0]} y {latitud_filtrada[1]}:")
        st.dataframe(data)
    else:
        st.error("La columna 'LATITUD' no se encuentra en el archivo.")
    
    # Extraer el año de la columna FECHA_UTC
    data['AÑO'] = data['FECHA_UTC'].astype(str).str[:4]
    
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
