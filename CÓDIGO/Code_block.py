import streamlit as st

# Título de la aplicación
st.title("Aplicación Simple con Streamlit")

# Subtítulo o descripción
st.write("Esta es una aplicación simple que saluda al usuario.")

# Entrada de texto para el nombre del usuario
nombre = st.text_input("Escribe tu nombre:")

# Mostrar el saludo al presionar el botón
if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! Bienvenido a la aplicación de Streamlit.")

