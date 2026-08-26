import pandas as pd
import re

def limpiar_sicoin(file):
    """
    Lee y limpia un archivo Excel exportado de SICOIN para estructurar jerarquías.
    Agrega manejo robusto de excepciones para archivos corruptos o mal estructurados.
    """
    try:
        df = pd.read_excel(file, header=None)
    except Exception as e:
        raise ValueError(f"El archivo está corrupto, protegido o no es un Excel válido: {str(e)}")

    if df.empty or len(df.columns) < 55:
        raise ValueError("El archivo no tiene la estructura de columnas de SICOIN esperada (al menos 55 columnas).")

    current_prog, current_subp, current_proy, current_act = "", "", "", ""
    flat_data = []

    for index, row in df.iterrows():
        # Saltamos el encabezado institucional y descriptivo de SICOIN
        if index < 20: 
            continue
            
        if pd.notna(row[0]) and pd.notna(row[5]) and pd.isna(row[1]):
            current_prog = f"{int(row[0])} - {row[5]}"
        elif pd.isna(row[0]) and pd.notna(row[1]) and pd.notna(row[8]) and pd.isna(row[5]):
            current_subp = f"{int(row[1])} - {row[8]}"
        elif pd.isna(row[0]) and pd.isna(row[1]) and pd.notna(row[2]) and pd.notna(row[10]):
            current_proy = f"{row[2]} - {row[10]}"
        elif pd.isna(row[0]) and pd.isna(row[1]) and pd.isna(row[2]) and pd.isna(row[3]) and pd.notna(row[4]) and pd.notna(row[10]):
            current_act = f"{int(row[4])} - {row[10]}"
        elif pd.notna(row[1]) and pd.notna(row[5]) and pd.notna(row[10]) and pd.notna(row[20]):
            if isinstance(row[5], str) and re.match(r'\d{2}-\d{4}-\d{4}', str(row[5])):
                renglon = int(row[1]) if isinstance(row[1], float) else row[1]
                flat_data.append({
                    'Programa': current_prog, 
                    'Subprograma': current_subp,
                    'Proyecto': current_proy, 
                    'Actividad': current_act,
                    'Renglón': str(renglon), 
                    'Fuente': row[5], 
                    'Descripción': row[10],
                    'Asignado': row[20], 
                    'Modificado': row[24], 
                    'Vigente': row[26],
                    'Compromiso': row[36], 
                    'Devengado': row[39], 
                    'Pagado': row[44],
                    'Saldo_Disponible': row[54]
                })

    if not flat_data:
        raise ValueError("No se encontraron renglones válidos en el archivo. Verifica que sea el reporte correcto de ejecución SICOIN.")

    df_limpio = pd.DataFrame(flat_data)
    
    # Conversión explícita para modelado en Power BI
    columnas_numericas = ['Asignado', 'Modificado', 'Vigente', 'Compromiso', 'Devengado', 'Pagado', 'Saldo_Disponible']
    for col in columnas_numericas:
        df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce').fillna(0.0)

    return df_limpio
