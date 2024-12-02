import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from shapely.geometry import Point
from streamlit_folium import st_folium


# Cargar dataset
file_path = "PA_FINAL/Dataset_1960_2023_sismo.csv"
data = pd.read_csv(file_path)
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


def visualizacion_anos(tipo):
    st.title("Visualización por Años")

    # Convertir fechas a datetime si no están ya en ese formato
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
            
            if not conteo_por_año.empty:
                colores = px.colors.qualitative.Set3  # Colores para los gráficos
                if tipo == "barras":
                    fig = px.bar(conteo_por_año, x=conteo_por_año.index, y=conteo_por_año.values, 
                                 color=conteo_por_año.index, 
                                 color_discrete_sequence=colores,
                                 labels={"x": "Año", "y": "Cantidad de Sismos"})
                elif tipo == "sector":
                    fig = px.pie(values=conteo_por_año.values, names=conteo_por_año.index,
                                 labels={"names": "Año", "values": "Cantidad de Sismos"})
                elif tipo == "lineas":
                    fig = px.line(conteo_por_año, x=conteo_por_año.index, y=conteo_por_año.values, 
                                  markers=True, 
                                  labels={"x": "Año", "y": "Cantidad de Sismos"})
                    fig.update_traces(marker=dict(size=10, color=colores[0]), line=dict(color=colores[1]))
                else:
                    st.error("Tipo de gráfico no soportado.")
                    return
                st.plotly_chart(fig)
                cantidad = datos_filtrados.shape[0]
                st.write(f"Cantidad de sismos : {cantidad}")
                
            else:
                st.warning("No hay datos para el rango de años seleccionado.")
        else:
            st.error("El año mínimo no puede ser mayor que el máximo.")

    elif filtro_tipo == "Por un solo año":
        año = st.number_input("Año:", value=int(data["AÑO"].min()), step=1)
        datos_filtrados = data[data["AÑO"] == año]
        conteo_por_mes = datos_filtrados["MES"].value_counts().sort_index()

        if not datos_filtrados.empty and not conteo_por_mes.empty:
            colores = px.colors.qualitative.Set3
            if tipo == "barras":
                fig = px.bar(conteo_por_mes, x=conteo_por_mes.index, y=conteo_por_mes.values,
                             color=conteo_por_mes.index, color_discrete_sequence=colores,
                             labels={"x": "Mes", "y": "Cantidad de Sismos"})
            elif tipo == "sector":
                fig = px.pie(values=conteo_por_mes.values, names=conteo_por_mes.index,
                             labels={"names": "Mes", "values": "Cantidad de Sismos"})
            elif tipo == "lineas":
                fig = px.line(conteo_por_mes, x=conteo_por_mes.index, y=conteo_por_mes.values,markers=True,
                              labels={"x": "Mes", "y": "Cantidad de Sismos"})
                fig.update_traces(marker=dict(size=10, color=colores[0]), line=dict(color=colores[1]))
            else:
                st.error("Tipo de gráfico no soportado.")
                return
            st.plotly_chart(fig)
            cantidad = datos_filtrados.shape[0]
            st.write(f"Cantidad de sismos : {cantidad}")
        else:
            st.warning("No hay datos para el año seleccionado.")


def visualizacion_magnitud(tipo):
    st.title("Visualización por Magnitud")
    filtro_tipo = st.radio("Selecciona el tipo de filtro:", ["Por rango de magnitudes", "Por magnitud única"])
    colores = px.colors.qualitative.Pastel
    if filtro_tipo == "Por rango de magnitudes":
        magnitud_min = st.number_input("Magnitud mínima:", value=float(data["MAGNITUD"].min()), step=0.1)
        magnitud_max = st.number_input("Magnitud máxima:", value=float(data["MAGNITUD"].max()), step=0.1)
        if magnitud_min <= magnitud_max:
            datos_filtrados = data[(data["MAGNITUD"] >= magnitud_min) & (data["MAGNITUD"] <= magnitud_max)]
            conteo_por_magnitud = datos_filtrados["MAGNITUD"].value_counts().sort_index()
            if tipo == "barras":
                fig = px.bar(conteo_por_magnitud, x=conteo_por_magnitud.index, y=conteo_por_magnitud.values, 
                             color=conteo_por_magnitud.index, 
                             color_discrete_sequence=colores,
                             labels={"x": "Magnitud", "y": "Cantidad de Sismos"})
            elif tipo == "sector":
                fig = px.pie(values=conteo_por_magnitud.values, names=conteo_por_magnitud.index,
                             labels={"names": "Magnitud", "values": "Cantidad de Sismos"})

            elif tipo == "lineas":
                fig = px.line(conteo_por_magnitud, x=conteo_por_magnitud.index, y=conteo_por_magnitud.values, 
                              markers=True, 
                              labels={"x": "Magnitud", "y": "Cantidad de Sismos"})
                fig.update_traces(marker=dict(size=10, color=colores[0]), line=dict(color=colores[1]))
            else:
                st.error("Tipo de gráfico no soportado.")
                return
            st.plotly_chart(fig)
            cantidad = datos_filtrados.shape[0]
            st.write(f"Cantidad de sismos : {cantidad}")
        else:
            st.error("La magnitud mínima no puede ser mayor que la máxima.")
    
    elif filtro_tipo == "Por magnitud única":
        magnitud = st.number_input("Ingresa una magnitud:", value=float(data["MAGNITUD"].min()), step=0.1)
        datos_filtrados = data[data["MAGNITUD"] == magnitud]
        if datos_filtrados.empty:
            st.write("No se encontraron datos para la magnitud seleccionada.")
        else:
            st.dataframe(datos_filtrados)
            cantidad = datos_filtrados.shape[0]
            st.write(f"Cantidad de sismos : {cantidad}")


def visualizacion_profundidad(tipo):
    st.title("Visualización por Profundidad")
    filtro_tipo = st.radio("Selecciona el tipo de filtro:", ["Por rango de profundidad", "Por valor único de profundidad"])

    if filtro_tipo == "Por rango de profundidad":
        profundidad_min = st.number_input("Profundidad mínima (km):", value=float(data["PROFUNDIDAD"].min()), step=0.1)
        profundidad_max = st.number_input("Profundidad máxima (km):", value=float(data["PROFUNDIDAD"].max()), step=0.1)
        if profundidad_min <= profundidad_max:
            datos_filtrados = data[(data["PROFUNDIDAD"] >= profundidad_min) & (data["PROFUNDIDAD"] <= profundidad_max)]
            conteo_por_profundidad = datos_filtrados["PROFUNDIDAD"].value_counts().sort_index()
            fig = px.bar(conteo_por_profundidad, x=conteo_por_profundidad.index, y=conteo_por_profundidad.values, labels={"x": "Profundidad", "y": "Cantidad de Sismos"})
            colores = px.colors.qualitative.Set3
            if tipo == "barras":
                fig = px.bar(conteo_por_profundidad, x=conteo_por_profundidad.index, y=conteo_por_profundidad.values,
                             color=conteo_por_profundidad.index, color_discrete_sequence=colores,
                             labels={"x": "Profundidad", "y": "Cantidad de Sismos"})
            elif tipo == "sector":
                fig = px.pie(values=conteo_por_profundidad.values, names=conteo_por_profundidad.index,
                             labels={"names": "Profundidad", "values": "Cantidad de Sismos"})
            elif tipo == "lineas":
                fig = px.line(conteo_por_profundidad, x=conteo_por_profundidad.index, y=conteo_por_profundidad.values,markers=True,
                              labels={"x": "Profundidad", "y": "Cantidad de Sismos"})
                fig.update_traces(marker=dict(size=10, color=colores[0]), line=dict(color=colores[1]))
            else:
                st.error("Tipo de gráfico no soportado.")
                return
            st.plotly_chart(fig)
            cantidad = datos_filtrados.shape[0]
            st.write(f"Cantidad de sismos : {cantidad}")
        else:
            st.error("La profundidad mínima no puede ser mayor que la máxima.")

    elif filtro_tipo == "Por valor único de profundidad":
        profundidad = st.number_input("Ingresa una profundidad (km):", value=float(data["PROFUNDIDAD"].min()), step=0.1)
        datos_filtrados = data[data["PROFUNDIDAD"] == profundidad]
        if datos_filtrados.empty:
            st.write("No se encontraron datos para la profundidad seleccionada.")
        else:
            st.dataframe(datos_filtrados)
            cantidad = datos_filtrados.shape[0]
            st.write(f"Cantidad de sismos : {cantidad}")


# MENU
# Función mapa
def mapa():
    # Configuración de la página
    """
    st.set_page_config(page_title="Mapa de Sismos en Perú", layout="wide")
    """
    
    # Título de la aplicación
    st.title("🌎 Mapa Interactivo de Sismos en Perú")

    # Cargar el archivo GeoJSON con los límites de los departamentos de Perú
    departamentos = gpd.read_file('PA_FINAL/departamentos_perú.geojson')
    if departamentos.crs is None or departamentos.crs != "EPSG:4326":
        departamentos = departamentos.to_crs("EPSG:4326")

    
    # Cargar el dataset de los sismos
    df = pd.read_csv('PA_FINAL/Dataset_1960_2023_sismo.csv')

    
    # Crear nuevas columnas para Año, Mes (como texto) y Día
    #df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y-%m-%d')
    df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y%m%d')
    df['AÑO'] = df['FECHA_UTC'].dt.year
    df['MES'] = df['FECHA_UTC'].dt.month_name(locale="es_ES")  # Nombres de meses en español
    df['DIA'] = df['FECHA_UTC'].dt.day

    # Crear geometrías de puntos a partir de LONGITUD y LATITUD
    geometry = [Point(xy) for xy in zip(df['LONGITUD'], df['LATITUD'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Realizar el join espacial para filtrar solo datos dentro de Perú
    joined_gdf = gpd.sjoin(gdf, departamentos, how="inner", predicate="intersects")

    # Crear columnas para separar el mapa y los filtros
    col1, col2 = st.columns([3, 1])  # Columna más ancha para el mapa (3), columna más estrecha para los filtros y gráficos (1)

    # Filtros de selección en la columna derecha
    with col2:
        st.markdown("### Filtros de Selección")
        
        # Filtro por departamento (con opción de seleccionar múltiples)
        filtro_departamento = st.multiselect("Selecciona un o más departamentos", options=["Todos"] + departamentos['NOMBDEP'].unique().tolist())
        
        # Filtro por rango de años y año único
        filtro_año_unico = st.selectbox("Selecciona un año", options=["Todos"] + sorted(df['AÑO'].unique().tolist()), index=0)
        rango_años = st.slider("Selecciona un rango de años", min_value=int(df['AÑO'].min()), max_value=int(df['AÑO'].max()), value=(int(df['AÑO'].min()), int(df['AÑO'].max())))
        
        # Filtro por mes
        filtro_mes = st.multiselect("Selecciona el mes", options=df['MES'].unique(), default=[])
        
        # Filtro por rango de magnitudes
        rango_magnitud = st.slider("Selecciona un rango de magnitudes", min_value=float(df['MAGNITUD'].min()), max_value=float(df['MAGNITUD'].max()), value=(float(df['MAGNITUD'].min()), float(df['MAGNITUD'].max())))

        # Filtro por rango de profundidad
        rango_profundidad = st.slider("Selecciona un rango de profundidad (km)", min_value=float(df['PROFUNDIDAD'].min()), max_value=float(df['PROFUNDIDAD'].max()), value=(float(df['PROFUNDIDAD'].min()), float(df['PROFUNDIDAD'].max())))

        # Filtrar los datos según los filtros seleccionados
        filtered_gdf = joined_gdf.copy()

        # Filtrar por departamento si no está en "Todos"
        if "Todos" not in filtro_departamento:
            filtered_gdf = filtered_gdf[filtered_gdf['NOMBDEP'].isin(filtro_departamento)]
        
        # Filtrar por año único
        if filtro_año_unico != "Todos":
            filtered_gdf = filtered_gdf[filtered_gdf['AÑO'] == int(filtro_año_unico)]
        
        # Filtrar por rango de años
        if rango_años:
            filtered_gdf = filtered_gdf[(filtered_gdf['AÑO'] >= rango_años[0]) & (filtered_gdf['AÑO'] <= rango_años[1])]
        
        # Filtrar por mes
        if filtro_mes:
            filtered_gdf = filtered_gdf[filtered_gdf['MES'].isin(filtro_mes)]
        
        # Filtrar por magnitud
        if rango_magnitud:
            filtered_gdf = filtered_gdf[(filtered_gdf['MAGNITUD'] >= rango_magnitud[0]) & (filtered_gdf['MAGNITUD'] <= rango_magnitud[1])]
        
        # Filtrar por profundidad
        if rango_profundidad:
            filtered_gdf = filtered_gdf[(filtered_gdf['PROFUNDIDAD'] >= rango_profundidad[0]) & (filtered_gdf['PROFUNDIDAD'] <= rango_profundidad[1])]

        # Mostrar la cantidad de puntos filtrados
        st.write(f"Cantidad de puntos filtrados: {len(filtered_gdf)}")

    # Crear un mapa centrado en Perú
    mapa_peru = folium.Map(location=[-9.19, -73.015], zoom_start=6)

    # Agregar los límites de los departamentos al mapa
    def estilo_departamento(feature):
        if feature['properties']['NOMBDEP'] in filtro_departamento or "Todos" in filtro_departamento:
            return {"fillColor": "#ff7800", "color": "red", "weight": 3, "fillOpacity": 0.5}
        return {"fillColor": "#14c7c1", "color": "black", "fillOpacity": 0.3}

    folium.GeoJson(
        departamentos,
        name="DEPARTAMENTO",
        style_function=estilo_departamento,
        tooltip=folium.GeoJsonTooltip(
            fields=["NOMBDEP"],
            aliases=["Departamento: "],
            localize=True
        )
    ).add_to(mapa_peru)

    # **Agregar esta condición para verificar si hay filtros seleccionados**
    if len(filtro_departamento) > 0 or len(filtro_mes) > 0 or filtro_año_unico != "Todos" or rango_años != (int(df['AÑO'].min()), int(df['AÑO'].max())) or rango_magnitud != (float(df['MAGNITUD'].min()), float(df['MAGNITUD'].max())) or rango_profundidad != (float(df['PROFUNDIDAD'].min()), float(df['PROFUNDIDAD'].max())):
        # Mostrar los puntos solo si hay al menos un filtro seleccionado
        if len(filtered_gdf) > 0:
            for _, row in filtered_gdf.iterrows():
                folium.CircleMarker(
                    location=[row['LATITUD'], row['LONGITUD']],
                    radius=5,
                    color="red",
                    fill=True,
                    fill_color="red",
                    fill_opacity=0.7,
                    popup=f"Departamento: {row['NOMBDEP']}<br>Año: {row['AÑO']}<br>Mes: {row['MES']}<br>Día: {row['DIA']}<br>Magnitud: {row['MAGNITUD']}<br>Profundidad: {row['PROFUNDIDAD']} km",
                ).add_to(mapa_peru)

    # Mostrar el mapa interactivo en la columna izquierda
    with col1:
        st.markdown("### Mapa de sismos en Perú")
        st_data = st_folium(mapa_peru, width=800, height=500)

    # Generar gráfico apilado por departamento y meses
    st.markdown("### Gráfico de Meses y Días por Departamento")
    if not filtered_gdf.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        pivot_data = filtered_gdf.pivot_table(
            index='NOMBDEP',
            columns='MES',
            values='DIA',
            aggfunc='count',
            fill_value=0
        )
        pivot_data.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
        ax.set_title('Distribución de Días por Departamento y Mes')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Cantidad de Días')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("No hay datos que coincidan con los filtros seleccionados.")


def conclusion():
    st.title("Catálogo Sísmico 1960 - 2023")
    # Conclusión  al tema
    st.markdown("""
    ### 📝 **En conclusión**, nuestro proyecto consiste en el desarrollo de un **dashboard interactivo** para visualizar y analizar datos sísmicos de **Perú** entre 1960 y 2023. 
    Utilizamos un dataset en formato CSV, procesamos los datos para asignar los sismos a departamentos específicos y ajustamos el formato de **fecha y hora** para mayor legibilidad.
    
    🌍 **Características principales:**
    - Filtros de selección para personalizar la visualización de los datos.
    - **Gráficos de barras** para el análisis de la distribución de sismos.
    - Un **mapa interactivo** para visualizar los sismos en las diferentes regiones de Perú.
    - **Menú de navegación** para facilitar la interacción del usuario.
    - Una **guía de usuario** detallada con imágenes ilustrativas para explicar el uso del dashboard.

    📊 **Impacto potencial:**
    - Este dashboard tiene un alto **potencial para la evaluación de riesgos sísmicos**, la **investigación geológica** y la **educación pública**.
    - La visualización interactiva de los datos sísmicos puede ayudar a identificar patrones y zonas de mayor riesgo.

    ⚠️ **Consideraciones importantes:**
    - Es fundamental asegurar la **implementación completa del código** para que todas las funcionalidades estén operativas.
    - Debemos tener en cuenta la **precisión de la geolocalización** y asegurar que el **dataset esté actualizado** para ofrecer datos precisos y relevantes.
""")


    st.image(
        "img/conclusion1.jpg",  # Ruta relativa a la imagen
        caption="El movimiento de la tierra nos impulsa a ser más conscientes y a valorar cada instante",
        use_container_width=True
    )

    st.markdown("""
    ### Recursos adicionales falta para conclusión
    - [Instituto Geofísico del Perú (IGP)](https://www.igp.gob.pe/)
    - [Servicio Geológico de los Estados Unidos (USGS)](https://earthquake.usgs.gov/)
    - [Wikipedia: Terremotos](https://es.wikipedia.org/wiki/Terremoto)
    """)

    st.info("🙌La naturaleza puede ser poderosa, pero la valentía y la solidaridad de las personas son indestructibles.🥰")


def foto():
    personas = [
        {"nombre": "", "info": "", "imagen": "img/noemi.png"},
        {"nombre": "", "info": "", "imagen": "img/carlos.png"},
        {"nombre": "", "info": "", "imagen": "img/nilda.png"},
        {"nombre": "", "info": "", "imagen": "img/bertil.png"}
    ]

    st.markdown("### 🧑‍💻 Equipo del Proyecto")

    # Crear un diseño en 2 filas y 2 columnas
    col1, col2 = st.columns(2)

    # Mostrar las primeras dos imágenes en la primera fila
    with col1:
        st.image(personas[0]["imagen"], width=450, caption=personas[0]["nombre"])
        st.markdown(f"**{personas[0]['nombre']}**")
        st.write(personas[0]["info"])

    with col2:
        st.image(personas[1]["imagen"], width=450, caption=personas[1]["nombre"])
        st.markdown(f"**{personas[1]['nombre']}**")
        st.write(personas[1]["info"])

    # Segunda fila con dos columnas
    col3, col4 = st.columns(2)

    with col3:
        st.image(personas[2]["imagen"], width=450, caption=personas[2]["nombre"])
        st.markdown(f"**{personas[2]['nombre']}**")
        st.write(personas[2]["info"])

    with col4:
        st.image(personas[3]["imagen"], width=450, caption=personas[3]["nombre"])
        st.markdown(f"**{personas[3]['nombre']}**")
        st.write(personas[3]["info"])



# MENÚ - ENCABEZADO
with st.container():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("img/logo_upch.png", width=800)  # Tamaño ajustado del logo
    with col2:
        # Crear el menú de navegación principal
        selected = option_menu(
            menu_title=None,  # Oculta el título del menú
            options=["Inicio", "Gráficos", "Mapa","Conclusión","Sobre nosotros"],  # Cambié a "Gráficos" como una opción principal
            icons=["house", "filter", "bar-chart-line"],  # Íconos para cada opción
            menu_icon="cast",  # Ícono del menú
            default_index=0,  # Página predeterminada
            orientation="horizontal",  # Orientación horizontal
            styles={
                "container": {"padding": "0!important", "background-color": "#333"},
                "icon": {"color": "orange", "font-size": "25px"}, # tamaño de icono
                "nav-link": {
                    "font-size": "18px", #tamaño letras
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "18px 28px",# tamaño de los botones
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

    # Submenú específico para cada tipo de gráfico
    tipo_grafico = option_menu(
        menu_title="Tipo de Gráfico",
        options=["Barras", "Sector Circular", "Líneas"],
        icons=["bar-chart", "pie-chart", "bar-chart-line", "picture", "graph-up"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#333"},
            "icon": {"color": "orange", "font-size": "14px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0px",
                "padding": "10px",
                "--hover-color": "#444",
            },
            "nav-link-selected": {"background-color": "#1199EE"},
        },
    )

    # Renderizar gráficos según las selecciones
    if selected_graph == "Por Año":
        if tipo_grafico == "Barras":
            visualizacion_anos(tipo="barras")
        elif tipo_grafico == "Sector Circular":
            visualizacion_anos(tipo="sector")
        elif tipo_grafico == "Líneas":
            visualizacion_anos(tipo="lineas")
    elif selected_graph == "Por Magnitud":
        if tipo_grafico == "Barras":
            visualizacion_magnitud(tipo="barras")
        elif tipo_grafico == "Sector Circular":
            visualizacion_magnitud(tipo="sector")
        elif tipo_grafico == "Líneas":
            visualizacion_magnitud(tipo="lineas")
    elif selected_graph == "Por Profundidad":
        if tipo_grafico == "Barras":
            visualizacion_profundidad(tipo="barras")
        elif tipo_grafico == "Sector Circular":
            visualizacion_profundidad(tipo="sector")
        elif tipo_grafico == "Líneas":
            visualizacion_profundidad(tipo="lineas")


elif selected == "Inicio":
    home_page()
elif selected == "Mapa":
    mapa()  
elif selected == "Conclusión":
    conclusion()
elif selected == "Sobre nosotros":
    foto()



