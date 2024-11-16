import streamlit as st
import folium as fl
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import plotly.express as px
import pandas as pd

# Análisis a nivel nacional
def visualizacion_a_nivel_nacional(archivo):
    # Leemos nuestro data set
    df = pd.read_excel(archivo)

    # Extraemos Año, Mes y Día de la columna Fecha_UTC del data set
    df["Anio"] = df["FECHA_UTC"].astype(str).str[:4]
    df["Mes"] = df["FECHA_UTC"].astype(str).str[4:6]
    df["Dia"] = df["FECHA_UTC"].astype(str).str[6:]

    # Encontramos el mínimo y el máximo de años comprendidos
    min_anio = df["Anio"].astype(int).min()
    max_anio = df["Anio"].astype(int).max()
    min_prof = df["PROFUNDIDAD"].astype(int).min()
    max_prof = df["PROFUNDIDAD"].astype(int).max()

    selected_min_anio = min_anio
    selected_max_anio = max_anio

    anios_comprendidos = []
    for i in range(min_anio, max_anio + 1):
        anios_comprendidos.append(i)

    st.markdown("<h2 style='text-align: left; color: #90ee90; font-family: monospace;'>Mapa de calor de eventos sísmicos por concurrencia en zonas geográficas y distribución por profundidad</h2>", unsafe_allow_html=True)

    st.markdown(
        '<div style="color: white;">'
        '<h>En esta sección, se presenta el análisis de la concurrencia de eventos sísmicos mediante un mapa de calor, '
        'junto con la distribución de estos por profundidad. Esta última, ya sea superficial, intermedia'
        ' o profunda, influye en la forma en que el sismo afecta a la superficie, por ende, el potencial destructivo.'
        ' A continuación, se ofrece la opción de búsqueda de eventos por fechas, ya sea de manera puntual o en rangos,'
        ' acompañada de una gráfica estadística para facilitar su comprensión.</h>'
        '</div>',
        unsafe_allow_html=True
    )
    st.divider()
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
        # Selección del tipo de búsqueda
        st.write("Seleccione la forma de búsqueda:")
        opcion = st.radio( 
            "Mostrar los eventos por",
            [ "**Mapa de calor**","**Distribución por porfundidad**"],
            captions = ["*con opción de búsqueda por fechas.*", "*con opción de búsqueda por fechas.*"],
            index=None)
        
    with col2:   
        # Mostraremos la información correspondiente a la opción seleccionada
        st.markdown(f"*Filtro de información de: {opcion}*")

    if opcion == None:
        # Inicializamos la previsualización con el mapa centrado 
        mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
        folium_static(mapa) 

    if opcion == "**Mapa de calor**":
        with col2:
            op_fecha1 = st.selectbox(
                "Por",
                ("años puntuales","ninguno"),
                index=None, placeholder="Seleccione . . .")
            
            if op_fecha1 == "años puntuales":
                fe_punt = st.multiselect(
                    "El año puntual de búsqueda es:",
                    anios_comprendidos, placeholder="elija")
                
                if fe_punt:
                    # Almacenamos los años puntuales seleccionados para después usarlos como filtro
                    fe_punt = list(map(int, fe_punt))

                    # Filtrarmos el DataFrame para incluir solo los años seleccionados
                    df_filtrado_opcion = df[df['Anio'].astype(int).isin(fe_punt)]

                    mapa = fl.Map(location=[df_filtrado_opcion['LATITUD'].mean(), df_filtrado_opcion['LONGITUD'].mean()], 
                                zoom_start=5.5, max_zoom=10, control_scale=True, width="100%", height="100%")

                    for index, row in df_filtrado_opcion.iterrows():
                        fl.Marker([row['LATITUD'], row['LONGITUD']],
                                    popup=f"Profundidad: {row['PROFUNDIDAD']} km\nMagnitud: {row['MAGNITUD']}").add_to(mapa)

                    heat_data = [[row['LATITUD'], row['LONGITUD']] for index, row in df_filtrado_opcion.iterrows()]
                    HeatMap(heat_data, name='Mapa de Calor', radius=50, max_zoom=15).add_to(mapa)
                    
                    # Construir la leyenda en HTML
                    legend_html = """
                        <div style="position: fixed; 
                                    bottom: 35px; left: 5px; width: 220px; height: 130px; 
                                    border:3px solid grey; z-index:9999; font-size:14px;
                                    background-color:white;text-align: center;
                                    border-radius: 6px;">
                            &nbsp; <span style="text-decoration: underline;", class="font-monospace">Leyenda</span> <br>
                            &nbsp; <span class="font-monospace">Baja concurrencia</span> &nbsp; 
                            <div style="width: 20px; height: 20px; background-color: green; display: inline-block;"></div>
                            &nbsp; <span class="font-monospace">Concurrencia moderada</span> &nbsp; 
                            <div style="width: 20px; height: 20px; background-color: orange; display: inline-block;"></div>
                            &nbsp; <span class="font-monospace">Alta concurrencia</span> &nbsp; 
                            <div style="width: 20px; height: 20px; background-color: red; display: inline-block;"></div>
                        </div>
                    """


                    # Convertir la leyenda HTML a un objeto de Folium
                    legend = fl.Element(legend_html)

                    # Agregar la leyenda al mapa
                    mapa.get_root().html.add_child(legend)
                
                    with col3:
                        st.components.v1.html(mapa._repr_html_(), width=710, height=470)
                else: 
                    with col3: 
                        mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                        folium_static(mapa)
            else: 
                with col3: 
                    mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                    folium_static(mapa) 

    if opcion == "**Distribución por porfundidad**":
        with col2:
            op_fecha2 = st.selectbox(
                "Por",
                ("rango de años", "ninguno"),
                index=None, placeholder="Seleccione . . .")
            

        if op_fecha2 == "rango de años":
            with col2:
                min_anio_option = st.selectbox('Selecciona el año mínimo', options=list(range(min_anio, max_anio + 1)), 
                                            index=None, placeholder="elija")
            if min_anio_option is not None:
                with col2:
                    if min_anio_option >= min_anio: 
                        max_anio_option = st.selectbox('Selecciona el año máximo', 
                                                    options=list(range(min_anio_option, max_anio + 1)))
                        max_anio = max_anio_option  
                        min_anio = min_anio_option      
                            
                        df_filtrado_opcion = df[
                            (df['Anio'].astype(int) >= min_anio) & (df['Anio'].astype(int) <= max_anio)
                        ]

                color_ub = ""                                   
                mapa = fl.Map(location=[df_filtrado_opcion['LATITUD'].mean(), df_filtrado_opcion['LONGITUD'].mean()], 
                            zoom_start=4.6, max_zoom=12, control_scale=True)

                for index, row in df_filtrado_opcion.iterrows():
                    if row['PROFUNDIDAD'] < 70:
                        color_ub = "red"
                    elif (row['PROFUNDIDAD'] >= 70) and (row['PROFUNDIDAD'] < 300):
                        color_ub = "orange"
                    elif row['PROFUNDIDAD'] >= 300:
                        color_ub = "green"
