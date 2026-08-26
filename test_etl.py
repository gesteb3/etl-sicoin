import pytest
import pandas as pd
import io
from etl import limpiar_sicoin

def test_limpiar_sicoin_invalid_excel():
    """Prueba que el ETL rechace un archivo corrupto o no válido."""
    invalid_file = io.BytesIO(b"Archivo de texto, no un excel")
    with pytest.raises(ValueError, match="El archivo está corrupto"):
        limpiar_sicoin(invalid_file)

def test_limpiar_sicoin_missing_columns():
    """Prueba que rechace DataFrames con menos de 55 columnas."""
    df = pd.DataFrame({'Col1': [1, 2], 'Col2': [3, 4]})
    file = io.BytesIO()
    df.to_excel(file, index=False, header=False)
    file.seek(0)
    with pytest.raises(ValueError, match="El archivo no tiene la estructura de columnas de SICOIN esperada"):
        limpiar_sicoin(file)

def test_limpiar_sicoin_no_data():
    """Prueba que rechace DataFrames válidos en columnas pero sin datos extraíbles."""
    # Creamos un DataFrame con 60 columnas y 30 filas, llenamos con 0s para que no se omitan columnas al exportar
    df = pd.DataFrame(0, index=range(30), columns=range(60))
    file = io.BytesIO()
    df.to_excel(file, index=False, header=False)
    file.seek(0)
    with pytest.raises(ValueError, match="No se encontraron renglones válidos en el archivo"):
        limpiar_sicoin(file)
