import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu


# Cargar datos
file_path = "Dataset_1960_2023_sismo.xlsx"
data = pd.read_excel(file_path)
data['FECHA_UTC'] = pd.to_datetime(data['FECHA_UTC'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
data['HORA_UTC'] = pd.to_datetime(data['HORA_UTC'], errors='coerce', format='%H%M%S').dt.time

# Funciones de las páginas
def home_page():
    st.title("Catálogo Sísmico 1960 - 2023")
    st.write("Bienvenido a la aplicación de análisis de sismos.")

    # Introducción al tema
    st.markdown("""
    ### ¿Qué es un sismo?
    Un sismo, también conocido como terremoto, es una vibración del terreno producida por la liberación súbita de energía acumulada en la corteza terrestre debido al movimiento de las placas tectónicas. Los sismos pueden ser leves y casi imperceptibles o devastadores, con graves consecuencias para la población y la infraestructura.

    ### Importancia del monitoreo de sismos
    - **Prevención**: El análisis de los datos sísmicos ayuda a entender las zonas de riesgo y diseñar construcciones más seguras.
    - **Ciencia**: Proporciona información clave sobre la dinámica del planeta Tierra.
    - **Educación**: Incrementa la conciencia pública sobre cómo actuar en caso de sismos.

    En esta aplicación, puedes explorar datos sísmicos registrados desde 1960 hasta 2023. Usa las opciones del menú para visualizar mapas, gráficos y aplicar filtros personalizados según tus intereses.
    """)

    st.image(
        "img/sismo.png",  # Ruta relativa a la imagen
        caption="El movimiento de la tierra nos impulsa a ser más conscientes y a valorar cada instante",
        use_container_width=True
    )

    st.markdown("""
    ### Recursos adicionales
    - [Instituto Geofísico del Perú (IGP)](https://www.igp.gob.pe/)
    - [Servicio Geológico de los Estados Unidos (USGS)](https://earthquake.usgs.gov/)
    - [Wikipedia: Terremotos](https://es.wikipedia.org/wiki/Terremoto)
    """)

    st.info("🙌La naturaleza puede ser poderosa, pero la valentía y la solidaridad de las personas son indestructibles.🥰")

def filtrado_cantidad():
    st.title("Filtrado por Cantidad de Sismos")
    columna = st.selectbox("Selecciona la columna para filtrar por valor único", ["ID", "PROFUNDIDAD", "MAGNITUD"])

    if pd.api.types.is_numeric_dtype(data[columna]):
        min_value = float(data[columna].min())
        max_value = float(data[columna].max())
        rango_min = st.number_input("Valor mínimo:", min_value=min_value, max_value=max_value, value=min_value)
        rango_max = st.number_input("Valor máximo:", min_value=min_value, max_value=max_value, value=max_value)

        if rango_min <= rango_max:
            datos_filtrados = data[(data[columna] >= rango_min) & (data[columna] <= rango_max)]
            st.write(f"Cantidad de sismos: {len(datos_filtrados)}")
            st.dataframe(datos_filtrados)
        else:
            st.error("El valor mínimo no puede ser mayor que el máximo.")

def visualizacion_anos():
    st.title("Visualización por Años")
    data["FECHA_UTC"] = pd.to_datetime(data["FECHA_UTC"], errors="coerce")
    data["AÑO"] = data["FECHA_UTC"].dt.year
    data["MES"] = data["FECHA_UTC"].dt.month

    filtro_tipo = st.radio("Selecciona el tipo de filtro:", ["Por rango de años", "Por un solo año"])
    if filtro_tipo == "Por rango de años":
        rango_min = st.number_input("Año mínimo:", value=int(data["AÑO"].min()), step=1)
        rango_max = st.number_input("Año máximo:", value=int(data["AÑO"].max()), step=1)
        if rango_min <= rango_max:
            datos_filtrados = data[(data["AÑO"] >= rango_min) & (data["AÑO"] <= rango_max)]
            conteo_por_año = datos_filtrados["AÑO"].value_counts().sort_index()
            fig = px.bar(conteo_por_año, x=conteo_por_año.index, y=conteo_por_año.values, labels={"x": "Año", "y": "Cantidad de Sismos"})
            st.plotly_chart(fig)
        else:
            st.error("El año mínimo no puede ser mayor que el máximo.")
    elif filtro_tipo == "Por un solo año":
        año = st.number_input("Año:", value=int(data["AÑO"].min()), step=1)
        datos_filtrados = data[data["AÑO"] == año]
        conteo_por_mes = datos_filtrados["MES"].value_counts().sort_index()
        fig = px.bar(conteo_por_mes, x=conteo_por_mes.index, y=conteo_por_mes.values, labels={"x": "Mes", "y": "Cantidad de Sismos"})
        st.plotly_chart(fig)

def visualizacion_magnitud():
    st.title("Visualización por Magnitud")
    filtro_tipo = st.radio("Selecciona el tipo de filtro:", ["Por rango de magnitudes", "Por magnitud única"])

    if filtro_tipo == "Por rango de magnitudes":
        magnitud_min = st.number_input("Magnitud mínima:", value=float(data["MAGNITUD"].min()), step=0.1)
        magnitud_max = st.number_input("Magnitud máxima:", value=float(data["MAGNITUD"].max()), step=0.1)
        if magnitud_min <= magnitud_max:
            datos_filtrados = data[(data["MAGNITUD"] >= magnitud_min) & (data["MAGNITUD"] <= magnitud_max)]
            conteo_por_magnitud = datos_filtrados["MAGNITUD"].value_counts().sort_index()
            fig = px.bar(conteo_por_magnitud, x=conteo_por_magnitud.index, y=conteo_por_magnitud.values, labels={"x": "Magnitud", "y": "Cantidad de Sismos"})
            st.plotly_chart(fig)
        else:
            st.error("La magnitud mínima no puede ser mayor que la máxima.")

    elif filtro_tipo == "Por magnitud única":
        magnitud = st.number_input("Ingresa una magnitud:", value=float(data["MAGNITUD"].min()), step=0.1)
        datos_filtrados = data[data["MAGNITUD"] == magnitud]
        if datos_filtrados.empty:
            st.write("No se encontraron datos para la magnitud seleccionada.")
        else:
            st.dataframe(datos_filtrados)

def visualizacion_profundidad():
    st.title("Visualización por Profundidad")
    filtro_tipo = st.radio("Selecciona el tipo de filtro:", ["Por rango de profundidad", "Por valor único de profundidad"])

    if filtro_tipo == "Por rango de profundidad":
        profundidad_min = st.number_input("Profundidad mínima (km):", value=float(data["PROFUNDIDAD"].min()), step=0.1)
        profundidad_max = st.number_input("Profundidad máxima (km):", value=float(data["PROFUNDIDAD"].max()), step=0.1)
        if profundidad_min <= profundidad_max:
            datos_filtrados = data[(data["PROFUNDIDAD"] >= profundidad_min) & (data["PROFUNDIDAD"] <= profundidad_max)]
            conteo_por_profundidad = datos_filtrados["PROFUNDIDAD"].value_counts().sort_index()
            fig = px.bar(conteo_por_profundidad, x=conteo_por_profundidad.index, y=conteo_por_profundidad.values, labels={"x": "Profundidad", "y": "Cantidad de Sismos"})
            st.plotly_chart(fig)
        else:
            st.error("La profundidad mínima no puede ser mayor que la máxima.")

    elif filtro_tipo == "Por valor único de profundidad":
        profundidad = st.number_input("Ingresa una profundidad (km):", value=float(data["PROFUNDIDAD"].min()), step=0.1)
        datos_filtrados = data[data["PROFUNDIDAD"] == profundidad]
        if datos_filtrados.empty:
            st.write("No se encontraron datos para la profundidad seleccionada.")
        else:
            st.dataframe(datos_filtrados)





# MENÚ - ENCABEZADO
with st.container():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("img/logo_upch.png", width=80)  # Tamaño ajustado del logo
    with col2:
        # Crear el menú de navegación principal
        selected = option_menu(
            menu_title=None,  # Oculta el título del menú
            options=["Inicio", "Filtros", "Gráficos", "Mapa"],  # Cambié a "Gráficos" como una opción principal
            icons=["house", "filter", "bar-chart-line"],  # Íconos para cada opción
            menu_icon="cast",  # Ícono del menú
            default_index=0,  # Página predeterminada
            orientation="horizontal",  # Orientación horizontal
            styles={
                "container": {"padding": "0!important", "background-color": "#333"},
                "icon": {"color": "orange", "font-size": "14px"}, # tamaño de icono
                "nav-link": {
                    "font-size": "18px", #tamaño letras
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "5px 10px",# tamaño de los botones
                    "white-space": "nowrap",
                    "--hover-color": "#444",
                },
                "nav-link-selected": {"background-color": "#1199EE"},
            },
        )

# Lógica para navegar entre las páginas y submenú
if selected == "Gráficos":
    selected_graph = option_menu(
        menu_title="Gráficos",  # Título del submenú
        options=["Por Año", "Por Magnitud", "Por Profundidad"],  # Opciones del submenú
        icons=["calendar", "bar-chart", "layers"],  # Íconos de submenú
        menu_icon="cast",  # Ícono del submenú
        default_index=0,  # Página predeterminada dentro del submenú
        orientation="vertical",  # Orientación vertical
        styles={
            "container": {"padding": "0!important", "background-color": "#444"},
            "icon": {"color": "orange", "font-size": "14px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0px",
                "padding": "10px",
                "--hover-color": "#555",
            },
            "nav-link-selected": {"background-color": "#1199EE"},
        },
    )

    # Cargar la página seleccionada dentro del submenú
    if selected_graph == "Por Año":
        visualizacion_anos()
    elif selected_graph == "Por Magnitud":
        visualizacion_magnitud()
    elif selected_graph == "Por Profundidad":
        visualizacion_profundidad()

elif selected == "Inicio":
    home_page()
elif selected == "Filtros":
    filtrado_cantidad()

