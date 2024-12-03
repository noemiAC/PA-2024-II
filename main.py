import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from shapely.geometry import Point
from streamlit_folium import st_folium
from PIL import Image

st.set_page_config(page_title="Sismos", page_icon="🌐", initial_sidebar_state="expanded", layout='wide')
# Cargar dataset
file_path = "Dataset_1960_2023_sismo.csv"
data = pd.read_csv(file_path)
data['FECHA_UTC'] = pd.to_datetime(data['FECHA_UTC'], format='%Y%m%d', errors='coerce').dt.strftime('%Y-%m-%d')
data['HORA_UTC'] = pd.to_datetime(data['HORA_UTC'], errors='coerce', format='%H%M%S').dt.time

# Funciones de las páginas
def home_page():
    st.title("Catálogo Sísmico 1960 - 2023")
    st.markdown("<h1 style='color:blue; text-align:center;'>BIENVENIDO A LA APLICACIÓN DE ANÁLISIS DE SISMOS</h1>", unsafe_allow_html=True)

    # Introducción al tema
    st.markdown("""
    ### ¿Qué es un sismo?
    Un sismo es una sacudida brusca y pasajera de la corteza terrestre que se produce por diversas causas, siendo las más comunes la actividad de fallas geológicas. También puede originarse por la fricción en el borde de placas tectónicas, procesos volcánicos, impactos de asteroides o explosiones nucleares subterráneas realizadas por el ser humano.

    El punto donde inicia el movimiento dentro de la Tierra se llama hipocentro o foco, y el lugar de la superficie terrestre directamente encima de este punto se denomina epicentro. Los sismos generan ondas sísmicas que se propagan desde el hipocentro y pueden causar fenómenos como desplazamientos de la corteza terrestre, tsunamis, corrimientos de tierras o actividad volcánica, dependiendo de su magnitud y origen.

    Se clasifican en varios tipos, como tectónicos, volcánicos, superficiales, y pueden medirse mediante escalas como la de Richter o la de magnitud de momento.

    ### Importancia del monitoreo de sismos
    - **Prevención**: El análisis de los datos sísmicos ayuda a entender las zonas de riesgo y diseñar construcciones más seguras.
    - **Ciencia**: Proporciona información clave sobre la dinámica del planeta Tierra.
    - **Educación**: Incrementa la conciencia pública sobre cómo actuar en caso de sismos.

    En esta aplicación, puedes explorar datos sísmicos registrados desde 1960 hasta 2023. Usa las opciones del menú para visualizar mapas, gráficos y aplicar filtros personalizados según tus intereses.
    """)
    img = Image.open("img/sismoportada.jpeg")
    img = img.resize((500, 600))  # Ajusta el valor de la altura según lo necesario
    # Mostrar la imagen redimensionada
    st.image(img)
    st.markdown("https://sinia.minam.gob.pe/sites/default/files/sial-sialtrujillo/archivos/public/docs/328.pdf")
    # st.image(
    #     "img/sismo.png",  # Ruta relativa a la imagen
    #     caption="El movimiento de la tierra nos impulsa a ser más conscientes y a valorar cada instante",
    #     use_container_width=True
    # )
    
    col1, col2 = st.columns([4,1])
    st.markdown("<h3>Componentes<h3>", unsafe_allow_html=True)
    # Conclusión  al tema
    with col1:
        st.markdown("""
        <p>
        El Perú, ubicado en el Cinturón de Fuego del Pacífico, es una región altamente sísmica. Esta actividad, combinada con un alto porcentaje de viviendas construidas mediante autoconstrucción o de antigüedad considerable, incrementa significativamente la vulnerabilidad de su población frente a eventos sísmicos. En este contexto, la plataforma de catálogo sísmico (1960-2023) que hemos desarrollado se convierte en una herramienta fundamental para informar a los usuarios sobre los sismos históricos en el país, facilitar la investigación sismológica con una base de datos homogénea y concientizar a la población sobre la recurrencia de estos eventos y la importancia de estar preparados [1].
        Nuestra plataforma cuenta con funcionalidades clave diseñadas para mejorar la comprensión de los usuarios. A través de mapas interactivos, es posible visualizar la distribución espacial de los sismos, diferenciados por colores según su magnitud o profundidad [2]. Los filtros dinámicos permiten realizar búsquedas específicas por magnitud, profundidad, fecha y departamento, mientras que gráficos como histogramas y dispersión ofrecen análisis detallados sobre la frecuencia de los sismos y la relación entre sus parámetros. Además, cada evento cuenta con información detallada sobre su fecha, hora, magnitud, profundidad, ubicación y, cuando sea posible, datos sobre daños ocasionados.
        El diseño intuitivo de la interfaz y la inclusión de recursos educativos sobre la sismología en Perú contribuyen a que esta herramienta sea accesible tanto para investigadores como para el público en general. Asimismo, se considera crucial mantener la base de datos actualizada con los últimos eventos sísmicos para garantizar la relevancia y efectividad de la plataforma [3].
        Con esta plataforma, buscamos no solo aumentar el conocimiento sobre la actividad sísmica en el Perú, sino también contribuir a la toma de decisiones informadas para la prevención y mitigación de desastres, fortaleciendo así la resiliencia de nuestras
        comunidades ante futuros eventos. sísmicos.</p>""", unsafe_allow_html=True)
    with col2: 
        st.image(
            "img/sismo_intro.png",  # Ruta relativa a la imagen
            caption="El movimiento de la tierra nos impulsa a ser más conscientes y a valorar cada instante",  use_container_width=True
        )
    col1, col2 = st.columns([1,4])
    with col1:
        img = Image.open("img/informesismo.png")
        img = img.resize((250, 300))  # Ajusta el valor de la altura según lo necesario
        # Mostrar la imagen redimensionada
        st.image(img)
    with col2:
        st.markdown("""
        <h5 style="color:blue; font-weight:bold; margin-bottom:5px;">Sismotectónica del sismo de Yauca del 28 de junio 2024 (M7.0) y niveles de sacudimiento del suelo - Informe Técnico N° 023-2024/IGP Ciencias de la Tierra Sólida</h5>
        
        <p style="font-size:1.2rem;">El 28 de junio de 2024, un sismo de magnitud 7.0 ocurrió a 54 km al SO de Yauca, Arequipa, con sacudidas percibidas hasta 500 km. Fue causado por la fricción entre las placas de Nazca y Sudamericana, generando 16 réplicas en 48 horas. El área de ruptura fue de 55 x 70 km. Aceleraciones de 150 cm/seg² en Yauca, Chala, Atiquipa y Bella Unión provocaron daños en viviendas de adobe y concreto, además de deslizamientos en la Panamericana Sur y vías secundarias.</p>
        
        """, unsafe_allow_html=True)

        st.markdown("""https://sigrid.cenepred.gob.pe/sigridv3/documento/17731.""")
    col1, col2 = st.columns([1,4])
    with col1:
        img = Image.open("img/mapasismico.png")
        img = img.resize((250, 300))  # Ajusta el valor de la altura según lo necesario
        # Mostrar la imagen redimensionada
        st.image(img)

    with col2:
        st.markdown("""
        <h5 style="color:blue; font-weight:bold; margin-bottom:5px;">MAPAS SÍSMICOS</h5>
        
        <p style="font-size:1rem;">El 19 de septiembre de 2013, el Instituto Geofísico del Perú (IGP) presentó el Mapa Sísmico del Perú en el Ministerio del Ambiente (MINAM), resultado de un trabajo de cuatro años concluido en 2012. Este documento detalla la distribución de eventos sísmicos entre 1960 y 2011, clasificados por profundidad, y permite identificar las zonas más afectadas por sismos en el país. Hernando Tavera, responsable del área de Sismología del IGP, destacó que las ciudades de la Costa son las más impactadas por sismos de intensidad regular y alta. En la sierra y la selva, las regiones con mayor actividad sísmica incluyen Moyobamba, Rioja, Ayacucho, Huancayo, Cusco y el Cañón del Colca, en Arequipa. Los mapas fueron entregados a direcciones del MINAM, como la Dirección de Investigación e Información Ambiental y la de Ordenamiento Territorial, para apoyar la gestión del riesgo y la preparación de la población ante sismos. La ceremonia contó con la participación de autoridades del IGP, MINAM, INDECI, RedPeIA, SOS Emergencias, la Municipalidad de Lima y otros organismos. </p>
        
        """, unsafe_allow_html=True)

        st.markdown("""https://sinia.minam.gob.pe/novedades/sismos-son-mas-frecuentes-fuertes-costa-pais""")
    col1, col2 = st.columns([1,4])
    with col1:
        img = Image.open("img/simulaciones.png")
        img = img.resize((250, 300))  # Ajusta el valor de la altura según lo necesario
        # Mostrar la imagen redimensionada
        st.image(img)
    with col2:
        st.markdown("""
        <h5 style="color:blue; font-weight:bold; margin-bottom:5px; ">Aprueban la Ejecución de Simulacros y Simulaciones y la Directiva “Ejecución de Simulacros y Simulaciones Ante Peligros Asociados a Fenómenos de Origen Natural”</h5>
        
        <p style="font-size:1.2rem;">reaccionar ante diversos escenarios (por bajas temperaturas; sismos seguido de tsunami; sismos seguido de fenómenos de geodinámica externa y por intensas precipitaciones pluviales) y la ejecución de las simulaciones tiene por objeto poner a prueba los Planes de Gestión Reactiva de los sectores, gobiernos regionales y locales, entidades públicas y privadas. .</p>
        
        """, unsafe_allow_html=True)

        st.markdown("""https://sinia.minam.gob.pe/sites/default/files/sinia/archivos/public/docs/rm_080-2016-pcm.pdf""")
    col1, col2 = st.columns([1,4])
    with col1:
        img = Image.open("img/frecuentes.png")
        img = img.resize((250, 300))  # Ajusta el valor de la altura según lo necesario
        # Mostrar la imagen redimensionada
        st.image(img)
    with col2:
        st.markdown("""
        <h5 style="color:blue; font-weight:bold; margin-bottom:5px;">Sismos son más frecuentes y fuertes en la costa del país</h5>
        
        <p style="font-size:1.2rem;">El Mapa Sísmico del Perú muestra sismos de magnitud ≥M4.0 desde 1960, según datos del IGP y Engdahl & Villaseñor. Clasifica eventos como superficiales, intermedios y profundos, según la profundidad de sus focos. Los sismos se originan en tres fuentes: contacto entre placas (como el terremoto de Pisco 2007, 8.0Mw), deformación continental (Moyobamba 1991, M6.0), y deformación oceánica (2011, M7.0). Predomina la actividad sísmica en el Centro y Sur. Este mapa es clave para delimitar zonas sismogénicas y prevenir riesgos.</p>
        
        """, unsafe_allow_html=True)

        st.markdown("""https://ultimosismo.igp.gob.pe/mapas-sismicos""")

    st.markdown("""
    ### Recursos adicionales
    - [El sitio web oficial de los registros administrativos del riesgo de desastres](https://sigrid.cenepred.gob.pe/sigridv3/documento/17731)
    - [El Sistema Nacional de Información Ambiental](https://sinia.minam.gob.pe/normas/aprueban-ejecucion-simulacros-simulaciones-directiva-ejecucion)
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
    departamentos = gpd.read_file('departamentos_perú.geojson')
    if departamentos.crs is None or departamentos.crs != "EPSG:4326":
        departamentos = departamentos.to_crs("EPSG:4326")

    
    # Cargar el dataset de los sismos
    df = pd.read_csv('Dataset_1960_2023_sismo.csv')

    
    # Crear nuevas columnas para Año, Mes (como texto) y Día
    #df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y-%m-%d')
    df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y%m%d')
    df['AÑO'] = df['FECHA_UTC'].dt.year
    # Convert to datetime
    # df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'])
    
    # Define a dictionary for month names in Spanish
    month_names = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    
    # Map the month numbers to their names
    df['MES'] = df['FECHA_UTC'].dt.month.map(month_names)
    # df['MES'] = df['FECHA_UTC'].dt.month_name(locale="es_ES")  # Nombres de meses en español
    
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
        filtro_departamento = st.multiselect("Selecciona un o más departamentos", options=["Todos"] + departamentos['NOMBDEP'].unique().tolist(), default=["Todos"])
        
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
        style_function=estilo_departamento
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
    st.markdown(""" 
    <h2>Análisis de Riesgos Sísmicos en Perú y el Desarrollo de una Plataforma de Catálogo Sísmico<h2>
    <h3>Conclusión<h5> """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    # Conclusión  al tema
    with col1:
        st.markdown("""
        <p style='font-size: 1.4rem;'>
        En conclusión, nuestro proyecto consiste en el desarrollo de un dashboard interactivo para visualizar y analizar datos sísmicos de Perú entre 1960 y 2023, utilizando un dataset en formato CSV. Realizamos un procesamiento de datos para asignar los sismos a departamentos específicos y ajustamos el formato de fecha y hora para mayor legibilidad. El dashboard, construido con Streamlit, ofrece funcionalidades como filtros de selección, gráficos de barras y un mapa interactivo. La interfaz incluye un menú de navegación para facilitar la interacción del usuario, y destacamos la importancia de una guía de usuario que explique el uso del dashboard con imágenes ilustrativas.
        Consideramos que el proyecto tiene un alto potencial para la evaluación de riesgos sísmicos, la investigación geológica y la educación pública. Sin embargo, es fundamental asegurar la implementación completa del código, tener en cuenta la precisión de la geolocalización y mantener el dataset actualizado.
        </p>""", unsafe_allow_html=True)

    with col2:
        st.image(
            "img/sismo_conclusion.png",  # Ruta relativa a la imagen
            caption="El movimiento de la tierra nos impulsa a ser más conscientes y a valorar cada instante", use_container_width=True
        )

    st.markdown("""
    ### Recursos adicionales
    - [El sitio web oficial de los registros administrativos del riesgo de desastres](https://sigrid.cenepred.gob.pe/sigridv3/documento/17731)
    - [El Sistema Nacional de Información Ambiental](https://sinia.minam.gob.pe/normas/aprueban-ejecucion-simulacros-simulaciones-directiva-ejecucion)
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
            icons=["house", "filter", "geo-alt-fill","body-text", "bi-people-fill"],  # Íconos para cada opción
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
