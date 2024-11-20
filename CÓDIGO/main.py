import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

# Título de la aplicación
st.title("Explorador de Sismos en Perú (1960-2023)")

# Descripción
st.markdown("""
Datos históricos de sismos en Perú desde 1960 hasta 2023.
Incluye visualización en un mapa interactivo y análisis de estadísticas por región, año y mes.
""")

# Crear un ejemplo de dataset de sismos
data = {
    "Año": [1965, 1998, 2020, 2010, 2018, 1998, 2010],
    "Mes": ["Marzo", "Julio", "Diciembre", "Mayo", "Octubre", "Julio", "Mayo"],
    "Latitud": [-12.0464, -13.1631, -8.112, -15.8402, -9.9306, -72.5459, -15.8402],
    "Longitud": [-77.0428, -72.5459, -79.032, -70.0219, -76.2428, -72.5459, -70.0219],
    "Magnitud": [6.5, 7.1, 5.8, 6.2, 5.0, 6.9, 6.3],
    "Lugar": ["Lima", "Cusco", "Trujillo", "Puno", "Huánuco", "Cusco", "Puno"]
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Mostrar dataset como tabla en el panel lateral
st.sidebar.header("Datos de Sismos")
st.sidebar.dataframe(df)

# Mapa interactivo con Pydeck
st.subheader("Mapa Interactivo de Sismos")

# Crear el mapa interactivo
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["Longitud", "Latitud"],
    get_radius=30000,
    get_fill_color="[255, 0, 0, 160]",
    pickable=True,  # Permite interacción con los puntos
)

view_state = pdk.ViewState(
    latitude=-9.19,  # Centro aproximado de Perú
    longitude=-75.0152,
    zoom=5,
    pitch=40,
)

# Mostrar mapa interactivo con detección de clics
tooltip = {"html": "<b>Lugar:</b> {Lugar} <br/><b>Magnitud:</b> {Magnitud}"}
r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
selected_data = st.pydeck_chart(r, use_container_width=True)

# Sección de filtros: Región, Año y Mes (distribuidos en columnas)
st.subheader("Filtros de Región, Año y Mes")
col1, col2, col3 = st.columns(3)

# Filtro de región
with col1:
    region_seleccionada = st.selectbox(
        "Selecciona una región:",
        options=df["Lugar"].unique()
    )

# Filtro de año
with col2:
    año_seleccionado = st.selectbox("Selecciona un año:", options=df["Año"].unique())

# Filtro de mes
with col3:
    mes_seleccionado = st.selectbox("Selecciona un mes:", options=df["Mes"].unique())

# Filtrar datos por región seleccionada
filtered_data_region = df[df["Lugar"] == region_seleccionada]

# Calcular la cantidad de sismos por año en la región seleccionada
cantidad_por_año_region = filtered_data_region.groupby("Año").size().reset_index(name="Cantidad de Sismos")

# Mostrar resultados para la región seleccionada
st.write(f"**Región seleccionada:** {region_seleccionada}")
st.write(f"**Cantidad total de sismos:** {filtered_data_region.shape[0]}")

# Gráfico de barras: Cantidad de sismos por año (en la región seleccionada)
fig_año_region = px.bar(
    cantidad_por_año_region,
    x="Año",
    y="Cantidad de Sismos",
    title=f"Cantidad de Sismos por Año en {region_seleccionada}",
    labels={"Cantidad de Sismos": "Cantidad"},
    text="Cantidad de Sismos"
)
fig_año_region.update_traces(textposition="outside")
st.plotly_chart(fig_año_region)

# Filtrar datos por año y mes seleccionados
filtered_data_año_mes = df[(df["Año"] == año_seleccionado) & (df["Mes"] == mes_seleccionado)]

# Mostrar los datos filtrados
st.write(f"**Sismos en {mes_seleccionado} de {año_seleccionado}:**")
st.dataframe(filtered_data_año_mes)

# Gráfico de barras: Magnitud de sismos en el mes y año seleccionados
if not filtered_data_año_mes.empty:
    fig_mes_año = px.bar(
        filtered_data_año_mes,
        x="Lugar",
        y="Magnitud",
        title=f"Magnitudes de Sismos en {mes_seleccionado} de {año_seleccionado}",
        labels={"Magnitud": "Magnitud"},
        text="Magnitud",
        color="Lugar"
    )
    fig_mes_año.update_traces(textposition="outside")
    st.plotly_chart(fig_mes_año)
else:
    st.warning("No se encontraron sismos en este mes y año.")

# Gráficos generales
st.subheader("Frecuencia de Sismos por Año")
fig_year = px.bar(df, x="Año", y="Magnitud", color="Lugar", title="Magnitud de Sismos por Año")
st.plotly_chart(fig_year)

st.subheader("Distribución de Sismos por Mes")
fig_month = px.bar(df, x="Mes", y="Magnitud", color="Lugar", title="Magnitud Promedio por Mes")
st.plotly_chart(fig_month)


