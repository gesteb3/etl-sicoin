import streamlit as st
import pandas as pd
from io import BytesIO
from etl import limpiar_sicoin

# --- INTERFAZ WEB MINIMALISTA (STREAMLIT) ---
st.set_page_config(page_title="Limpiador SICOIN", page_icon="📊")

st.title("Procesador de Ejecución Presupuestaria")
st.write("Sube el reporte de egresos exportado de SICOIN (.xls) para estructurarlo para Power BI.")

# 1. Botón para subir archivo
archivo_subido = st.file_uploader("Selecciona el archivo Excel", type=["xls", "xlsx"])

if archivo_subido is not None:
    try:
        with st.spinner('Procesando datos y estructurando jerarquías...'):
            # Ejecutar la limpieza
            df_limpio = limpiar_sicoin(archivo_subido)
            
            st.success(f"¡Limpieza exitosa! Se extrajeron {len(df_limpio)} renglones.")
            
            # Mostrar una vista previa a la gerencia
            st.write("Vista previa de los datos estructurados:")
            st.dataframe(df_limpio.head(5))

            # 2. Preparar el archivo limpio para descarga en memoria (sin guardar basura en el disco)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_limpio.to_excel(writer, index=False, sheet_name='Ejecucion_Limpia')
            datos_procesados = output.getvalue()

            # 3. Botón para descargar
            st.download_button(
                label="📥 Descargar Excel Limpio para Power BI",
                data=datos_procesados,
                file_name="Ejecucion_Egresos_Limpia.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error al procesar el archivo: Asegúrate de que sea el formato correcto de SICOIN. Detalle técnico: {e}")