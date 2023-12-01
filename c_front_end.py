# Importar el backend
import b_backend
import streamlit as st

# Configuración de Streamlit
st.title("CBOL 🤖")
st.write("Puedes hacerme las preguntas que necesites sobre errores de equipos de frío")

# Función para dividir el texto en líneas cada 50 caracteres con espacios
def dividir_texto(texto, max_caracteres=50):
    palabras = texto.split()
    lineas = []
    linea_actual = ''
    for palabra in palabras:
        if len(linea_actual + palabra) <= max_caracteres:
            linea_actual += palabra + ' '
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + ' '
    lineas.append(linea_actual.strip())
    return lineas

# Inicializar listas en el estado de la sesión para preguntas y respuestas
if 'preguntas' not in st.session_state:
    st.session_state.preguntas = []
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []

# Función para hacer la consulta y manejar el clic en el botón Enviar
def click():
    if st.session_state.user != '':
        # Concatenar la descripción de error a la pregunta del usuario
        pregunta = f"{st.session_state.user} , la pregunta anterior es sobre el numero de codigo de error que esta presente en la columna numero, cuando te pregunte algo como: error 1, 1, error 2, 2, etc., debes de responder con la descipcion del error que esta en la columna descripcion y la accion que se debe de tomar en la columna accion del el numero que coninicida con el numero que te estan preguntando."
        respuesta = b_backend.consulta(pregunta)

        st.session_state.preguntas.append(pregunta)
        st.session_state.respuestas.append(respuesta)

        # Limpiar el input de usuario después de enviar la pregunta
        st.session_state.user = ''

# Sección para crear botones de preguntas frecuentes
preguntas_frecuentes = ["¿Cuál es el código de error 1?", "¿Cómo soluciono el error 2?", "¿Cual es la solucion mas comun?"]

for pregunta in preguntas_frecuentes:
    if st.button(pregunta):
        # Al presionar el botón, enviar la pregunta al backend y obtener la respuesta
        respuesta = b_backend.consulta(pregunta)

        # Agregar la pregunta y respuesta al historial
        st.session_state.preguntas.append(pregunta)
        st.session_state.respuestas.append(respuesta)

# Crear el formulario de Streamlit
with st.form('my-form'):
    query = st.text_input('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
    submit_button = st.form_submit_button('Enviar', on_click=click)

# Visualizar preguntas y respuestas
if st.session_state.preguntas:
    chat_container = st.container()
    for i in range(len(st.session_state.respuestas)-1, -1, -1):
        with chat_container:
            st.text(f'Tú: {st.session_state.preguntas[i]}')
            respuesta = st.session_state.respuestas[i]
            # Dividir la respuesta en líneas cada 50 caracteres con espacios
            lineas_respuesta = dividir_texto(respuesta)
            # Mostrar toda la respuesta como un solo párrafo
            st.write(f'CBOL 🤖: {" ".join(lineas_respuesta)}')

    # Opción para continuar la conversación
    continuar_conversacion = st.checkbox('¿Quieres hacer otra pregunta?')
    if not continuar_conversacion:
        st.session_state.preguntas = []
        st.session_state.respuestas = []