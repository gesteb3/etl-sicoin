# Limpiador SICOIN

Aplicación web minimalista construida con [Streamlit](https://streamlit.io/) que procesa reportes de ejecución presupuestaria (en formato Excel) exportados de SICOIN. Extrae la información estructurando las jerarquías (Programa, Subprograma, Proyecto, Actividad y Renglón) y exporta un archivo Excel limpio listo para ser consumido en herramientas como Power BI.

## Requisitos

- Python 3.7 o superior.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd etl-sicoingl
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   Asegúrate de tener instalados los siguientes paquetes, puedes instalarlos ejecutando:
   ```bash
   pip install streamlit pandas openpyxl pytest
   ```

## Uso

1. Inicia la aplicación ejecutando el siguiente comando:
   ```bash
   streamlit run app.py
   ```
2. Se abrirá automáticamente una pestaña en tu navegador web.
3. Sube el reporte de SICOIN (formato `.xls` o `.xlsx`).
4. Revisa la vista previa de los datos procesados.
5. Haz clic en "Descargar Excel Limpio para Power BI" para obtener el resultado.

## Pruebas
Puedes ejecutar las pruebas unitarias utilizando pytest:
```bash
pytest test_etl.py
```
