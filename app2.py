import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
@st.cache
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Ruta al archivo Excel
file_path = "datos_paises_procesados.xlsx"
data = load_data(file_path)

# Configuración de la página
st.set_page_config(page_title="Visualización de Datos de Países", layout="wide")

# Páginas de la aplicación
def pagina_descripcion():
    st.title("Descripción del Proyecto")
    st.write("""
    Esta aplicación utiliza datos de países preprocesados en un archivo Excel para realizar análisis y visualizaciones interactivas.
    """)
    st.write("### Datos del Proyecto:")
    st.dataframe(data.head())
    st.write("Fuente de datos: **Archivo Excel preprocesado**.")

def pagina_interaccion():
    st.title("Interacción con los Datos")
    st.write("### Datos Originales:")
    st.dataframe(data)

    st.write("### Estadísticas Básicas")
    columna = st.selectbox("Seleccione una columna para analizar", options=data.select_dtypes(include=["int64", "float64"]).columns)
    if columna:
        st.write(f"**Media:** {data[columna].mean()}")
        st.write(f"**Mediana:** {data[columna].median()}")
        st.write(f"**Desviación Estándar:** {data[columna].std()}")

    st.write("### Ordenar Datos")
    columna_orden = st.selectbox("Seleccione una columna para ordenar", options=data.columns)
    orden = st.radio("Orden:", ["Ascendente", "Descendente"])
    if columna_orden:
        datos_ordenados = data.sort_values(by=columna_orden, ascending=(orden == "Ascendente"))
        st.dataframe(datos_ordenados)

    st.write("### Filtrar Datos")
    filtro_columna = st.selectbox("Seleccione una columna numérica para filtrar", options=data.select_dtypes(include=["int64", "float64"]).columns)
    if filtro_columna:
        min_val = float(data[filtro_columna].min())
        max_val = float(data[filtro_columna].max())
        rango = st.slider("Seleccione un rango", min_val, max_val, (min_val, max_val))
        datos_filtrados = data[(data[filtro_columna] >= rango[0]) & (data[filtro_columna] <= rango[1])]
        st.dataframe(datos_filtrados)

        # Botón para descargar
        st.download_button("Descargar datos filtrados", datos_filtrados.to_csv(index=False), "datos_filtrados.csv")

def pagina_graficos():
    st.title("Visualización de Datos")
    
    st.write("### Crear un Gráfico")
    tipo_grafico = st.selectbox("Seleccione un tipo de gráfico", options=["Barras", "Línea", "Dispersión", "Pastel"])
    x_col = st.selectbox("Seleccione la variable para el eje X", options=data.select_dtypes(include=["int64", "float64"]).columns)
    y_col = st.selectbox("Seleccione la variable para el eje Y", options=data.select_dtypes(include=["int64", "float64"]).columns)

    if tipo_grafico and x_col and y_col:
        fig, ax = plt.subplots()
        if tipo_grafico == "Barras":
            ax.bar(data[x_col], data[y_col])
        elif tipo_grafico == "Línea":
            ax.plot(data[x_col], data[y_col])
        elif tipo_grafico == "Dispersión":
            ax.scatter(data[x_col], data[y_col])
        elif tipo_grafico == "Pastel":
            data.groupby(x_col)[y_col].sum().plot.pie(ax=ax, autopct="%1.1f%%")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        st.pyplot(fig)

        # Botón para descargar gráfico
        st.download_button("Descargar gráfico", fig.savefig, "grafico.png")

# Mapeo de páginas
paginas = {
    "Descripción del Proyecto": pagina_descripcion,
    "Interacción con los Datos": pagina_interaccion,
    "Visualización de Datos": pagina_graficos,
}

# Menú de navegación
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Seleccione una página", list(paginas.keys()))

# Ejecutar la página seleccionada
paginas[opcion]()
