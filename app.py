import streamlit as st
import pandas as pd
import os

# Configuración inicial
st.set_page_config(page_title="Consulta de Base", layout="wide")

st.title("📊 Explorador de Asistencias")

# 1. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    ruta = "base_limpia.xlsx"
    if not os.path.exists(ruta):
        st.error(f"Error: No se encontró el archivo {ruta}")
        return pd.DataFrame()
    
    df = pd.read_excel(ruta)
    # Limpiar espacios en blanco de los nombres de columnas
    df.columns = df.columns.str.strip()
    return df

df = cargar_datos()

if not df.empty:
    # 2. SIDEBAR DE FILTROS
    st.sidebar.header("🔎 Búsqueda y filtros")
    
    busqueda = st.sidebar.text_input("Buscar (nombre, dni, actividad, etc.)")
    
    # Filtros únicos
    actividad = st.sidebar.multiselect("Actividad", df["nombre_actividad"].dropna().unique())
    categoria = st.sidebar.multiselect("Categoría", df["categoria"].dropna().unique())
    mes = st.sidebar.multiselect("Mes", df["mes"].dropna().unique())

    # 3. LÓGICA DE FILTRADO
    df_filtrado = df.copy()

    if actividad:
        df_filtrado = df_filtrado[df_filtrado["nombre_actividad"].isin(actividad)]

    if categoria:
        df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categoria)]

    if mes:
        df_filtrado = df_filtrado[df_filtrado["mes"].isin(mes)]

    if busqueda:
        # Filtra si la palabra buscada está en cualquier columna
        mask = df_filtrado.astype(str).apply(
            lambda row: row.str.contains(busqueda, case=False, na=False).any(), 
            axis=1
        )
        df_filtrado = df_filtrado[mask]

    # 4. RESULTADOS
    st.write(f"📌 Registros encontrados: {len(df_filtrado)}")
    
    # Esta es la tabla que responde a los filtros
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.info("Por favor, asegúrate de que el archivo 'base_limpia.xlsx' esté en la misma carpeta que este script.")
