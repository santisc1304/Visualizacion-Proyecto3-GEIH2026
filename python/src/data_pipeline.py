"""
data_pipeline.py
================
Pipeline de extracción, consolidación, ponderación muestral (FEX_C18)
y agregación analítica de la Gran Encuesta Integrada de Hogares (GEIH) 2026 (Enero - Julio)
para el Proyecto 3: Narrativa Visual Integrada (Universidad Externado de Colombia).

Autores: Santiago Sandoval & Sebastián Ramos
"""

import os
import glob
import json
import pandas as pd
import numpy as np

# Rutas base relativas
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
WEB_JS_DIR = os.path.join(BASE_DIR, "web", "js")

DPTO_DICT = {
    5: "Antioquia", 8: "Atlántico", 11: "Bogotá D.C.", 13: "Bolívar", 15: "Boyacá",
    17: "Caldas", 18: "Caquetá", 19: "Cauca", 20: "Cesar", 23: "Córdoba",
    25: "Cundinamarca", 27: "Chocó", 41: "Huila", 44: "La Guajira", 47: "Magdalena",
    50: "Meta", 52: "Nariño", 54: "Norte de Santander", 63: "Quindío", 66: "Risaralda",
    68: "Santander", 70: "Sucre", 73: "Tolima", 76: "Valle del Cauca", 81: "Arauca",
    85: "Casanare", 86: "Putumayo", 88: "San Andrés", 91: "Amazonas", 94: "Guainía",
    95: "Guaviare", 97: "Vaupés", 99: "Vichada"
}

def map_sector(rama):
    if pd.isna(rama):
        return "Otros"
    try:
        r = int(rama)
    except:
        return "Otros"
    if 1 <= r <= 3:
        return "Agropecuario"
    elif 5 <= r <= 9:
        return "Minería"
    elif 10 <= r <= 33:
        return "Industria manufacturera"
    elif 35 <= r <= 39:
        return "Servicios públicos"
    elif 41 <= r <= 43:
        return "Construcción"
    elif 45 <= r <= 47:
        return "Comercio"
    elif 49 <= r <= 53:
        return "Transporte y almacenamiento"
    elif 55 <= r <= 56:
        return "Alojamiento y comida"
    elif 58 <= r <= 63:
        return "Información y comunicaciones"
    elif 64 <= r <= 66:
        return "Actividades financieras"
    elif 68 <= r <= 82:
        return "Servicios profesionales e inmobiliarios"
    elif r == 84:
        return "Administración pública"
    elif r == 85:
        return "Educación"
    elif 86 <= r <= 88:
        return "Salud y asistencia social"
    elif 90 <= r <= 93:
        return "Arte y entretenimiento"
    elif 94 <= r <= 99:
        return "Otros servicios"
    else:
        return "Otros"

def map_age_group(edad):
    if pd.isna(edad):
        return "No especificado"
    e = int(edad)
    if e < 18:
        return "Menor de 18 años"
    elif 18 <= e <= 24:
        return "18 a 24 años"
    elif 25 <= e <= 34:
        return "25 a 34 años"
    elif 35 <= e <= 54:
        return "35 a 54 años"
    else:
        return "55 años o más"

def map_tipo_trabajador(p6430):
    if p6430 == 4:
        return "Cuenta propia"
    elif p6430 in [1, 2]:
        return "Asalariado"
    elif p6430 == 3:
        return "Empleado doméstico"
    elif p6430 == 5:
        return "Patrón o empleador"
    elif p6430 in [6, 7]:
        return "Trabajador familiar sin remuneración"
    else:
        return "Otros"

def load_and_consolidate_geih():
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio']
    all_rows = []
    
    print("Iniciando consolidación de microdatos GEIH 2026 (Enero a Julio)...")
    for m in months:
        f_ocu = os.path.join(RAW_DATA_DIR, f"{m} 2026", "CSV", "Ocupados.CSV")
        f_cg1 = os.path.join(RAW_DATA_DIR, f"{m} 2026", "CSV", "Características generales, seguridad social en salud y educación.CSV")
        f_cg2 = os.path.join(RAW_DATA_DIR, f"{m} 2026", "CSV", "Capítulos de características generales, seguridad social en salud y educación.CSV")
        
        f_cg = f_cg1 if os.path.exists(f_cg1) else f_cg2
        if not os.path.exists(f_ocu) or not os.path.exists(f_cg):
            print(f"Advertencia: Archivos no encontrados para {m}")
            continue
            
        print(f"  Procesando {m} 2026...")
        df_o = pd.read_csv(
            f_ocu, sep=';', encoding='latin1',
            usecols=['DIRECTORIO', 'SECUENCIA_P', 'ORDEN', 'HOGAR', 'MES', 'DPTO', 'P6430', 'INGLABO', 'P6500', 'RAMA2D_R4', 'FEX_C18']
        )
        df_c = pd.read_csv(
            f_cg, sep=';', encoding='latin1',
            usecols=['DIRECTORIO', 'SECUENCIA_P', 'ORDEN', 'HOGAR', 'P6040', 'P3271']
        )
        
        merged = pd.merge(df_o, df_c, on=['DIRECTORIO', 'SECUENCIA_P', 'ORDEN', 'HOGAR'])
        all_rows.append(merged)
        
    df = pd.concat(all_rows, ignore_index=True)
    print(f"Total registros ocupados consolidados: {len(df):,}")
    
    # Transformaciones y mapeos
    df['DPTO'] = df['DPTO'].astype(int)
    df['DPTO_Nombre'] = df['DPTO'].map(DPTO_DICT).fillna("Desconocido")
    df['SectorEconomico'] = df['RAMA2D_R4'].apply(map_sector)
    df['GrupoEdad'] = df['P6040'].apply(map_age_group)
    df['Sexo'] = df['P3271'].map({1: "Hombre", 2: "Mujer"}).fillna("No especificado")
    df['TipoTrabajador'] = df['P6430'].apply(map_tipo_trabajador)
    
    return df

def generate_datasets_and_metrics():
    df = load_and_consolidate_geih()
    
    # 1. Dataset P1 Referencia (105.542 registros)
    df_p1 = df[(df['P6430'].isin([1, 2, 3])) & (df['P6500'] > 0)].copy()
    print(f"\n[Dataset P1 Verificación]")
    print(f"Total registros: {len(df_p1):,} (Esperado: 105,542)")
    print(f"Ingreso Promedio P6500: ${df_p1['P6500'].mean():,.0f} (Esperado: $2,474,617)")
    print(f"CV P6500: {df_p1['P6500'].std() / df_p1['P6500'].mean():.4f} (Esperado: 1.0105)")
    
    # 2. Dataset Integrado Ciudadano para Proyecto 3:
    # Compara Cuenta propia (independientes) vs Asalariados con ingresos laborales válidos (INGLABO > 0)
    # y adultos de 18 años o más
    df_ciudadano = df[(df['TipoTrabajador'].isin(['Cuenta propia', 'Asalariado'])) & (df['INGLABO'] > 0) & (df['P6040'] >= 18)].copy()
    print(f"\n[Dataset Ciudadano Proyecto 3]")
    print(f"Total registros adultos analizados: {len(df_ciudadano):,}")
    print(df_ciudadano['TipoTrabajador'].value_counts())
    
    # Guardar en formato Parquet de alta velocidad y compresión
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    parquet_path = os.path.join(PROCESSED_DIR, "base_geih_ciudadana_analisis.parquet")
    df_ciudadano.to_parquet(parquet_path, index=False)
    print(f"Guardado dataset Parquet en: {parquet_path}")
    
    # También guardar una muestra representativa en CSV para interoperabilidad directa si se requiere
    sample_csv = os.path.join(PROCESSED_DIR, "base_geih_ciudadana_sample.csv")
    df_ciudadano.sample(min(20000, len(df_ciudadano)), random_state=42).to_csv(sample_csv, index=False)
    print(f"Guardada muestra CSV en: {sample_csv}")
    
    # 3. Métricas Departamentales para Cartografía en R (sf / tmap)
    dept_metrics = []
    for dpto_code, dpto_name in DPTO_DICT.items():
        sub_dpto = df_ciudadano[df_ciudadano['DPTO'] == dpto_code]
        if len(sub_dpto) == 0:
            continue
        
        # Independientes
        indep = sub_dpto[sub_dpto['TipoTrabajador'] == 'Cuenta propia']
        asal = sub_dpto[sub_dpto['TipoTrabajador'] == 'Asalariado']
        
        n_indep = len(indep)
        n_asal = len(asal)
        
        if n_indep > 0:
            # Métricas ponderadas con FEX_C18
            w_indep = indep['FEX_C18']
            mean_indep_w = np.average(indep['INGLABO'], weights=w_indep)
            var_indep_w = np.average((indep['INGLABO'] - mean_indep_w)**2, weights=w_indep)
            std_indep_w = np.sqrt(var_indep_w)
            cv_indep_w = std_indep_w / mean_indep_w if mean_indep_w > 0 else 0
            med_indep = indep['INGLABO'].median()
        else:
            mean_indep_w, std_indep_w, cv_indep_w, med_indep = 0, 0, 0, 0
            
        if n_asal > 0:
            w_asal = asal['FEX_C18']
            mean_asal_w = np.average(asal['INGLABO'], weights=w_asal)
            med_asal = asal['INGLABO'].median()
        else:
            mean_asal_w, med_asal = 0, 0
            
        brecha_relativa = ((mean_indep_w - mean_asal_w) / mean_asal_w) * 100 if mean_asal_w > 0 else 0
        
        # Índice de Predictibilidad Territorial (0 a 100, donde mayor es más predecible / menor CV)
        # Normalizado acotando CV típico entre 0.4 y 1.6
        ind_predictibilidad = max(0, min(100, (1.6 - cv_indep_w) / (1.6 - 0.4) * 100))
        
        dept_metrics.append({
            "DPTO_CCDGO": str(dpto_code).zfill(2),
            "DPTO": dpto_code,
            "DPTO_Nombre": dpto_name,
            "N_Independientes": n_indep,
            "N_Asalariados": n_asal,
            "Poblacion_Indep_Expandida": int(indep['FEX_C18'].sum()) if n_indep > 0 else 0,
            "Ingreso_Medio_Indep": round(mean_indep_w, 2),
            "Mediana_Indep": round(med_indep, 2),
            "CV_Indep_Ponderado": round(cv_indep_w, 4),
            "Ingreso_Medio_Asal": round(mean_asal_w, 2),
            "Mediana_Asal": round(med_asal, 2),
            "Brecha_Relativa_Pct": round(brecha_relativa, 2),
            "Indice_Predictibilidad": round(ind_predictibilidad, 2)
        })
        
    df_dept = pd.DataFrame(dept_metrics)
    dept_csv_path = os.path.join(PROCESSED_DIR, "metricas_departamentales.csv")
    df_dept.to_csv(dept_csv_path, index=False, encoding='utf-8')
    print(f"Guardadas métricas departamentales en: {dept_csv_path} ({len(df_dept)} departamentos)")
    
    # 4. Métricas de Perfiles para el Simulador Interactivo Web
    # Cruces por SectorEconomico x GrupoEdad para trabajadores independientes
    profiles = []
    indep_all = df_ciudadano[df_ciudadano['TipoTrabajador'] == 'Cuenta propia']
    asal_all = df_ciudadano[df_ciudadano['TipoTrabajador'] == 'Asalariado']
    
    sectors = [
        "Educación", "Comercio", "Construcción", "Agropecuario",
        "Alojamiento y comida", "Industria manufacturera",
        "Transporte y almacenamiento", "Información y comunicaciones",
        "Servicios profesionales e inmobiliarios", "Arte y entretenimiento", "Minería"
    ]
    age_groups = ["18 a 24 años", "25 a 34 años", "35 a 54 años", "55 años o más"]
    
    for sec in sectors:
        for age in age_groups:
            sub_ind = indep_all[(indep_all['SectorEconomico'] == sec) & (indep_all['GrupoEdad'] == age)]
            sub_as = asal_all[(asal_all['SectorEconomico'] == sec) & (asal_all['GrupoEdad'] == age)]
            
            n_sub = len(sub_ind)
            if n_sub < 10:
                continue
                
            w = sub_ind['FEX_C18']
            m_ind = np.average(sub_ind['INGLABO'], weights=w)
            v_ind = np.average((sub_ind['INGLABO'] - m_ind)**2, weights=w)
            cv_ind = np.sqrt(v_ind) / m_ind if m_ind > 0 else 0
            p25 = sub_ind['INGLABO'].quantile(0.25)
            p50 = sub_ind['INGLABO'].median()
            p75 = sub_ind['INGLABO'].quantile(0.75)
            
            m_as = np.average(sub_as['INGLABO'], weights=sub_as['FEX_C18']) if len(sub_as) > 0 else m_ind
            brecha = ((m_ind - m_as) / m_as * 100) if m_as > 0 else 0
            
            # Clasificación semántica de estabilidad
            if cv_ind < 0.75:
                estatus = "Estabilidad Alta"
                colchon_meses = "2 a 3 meses"
                color_hex = "#16A34A" # Verde
            elif cv_ind <= 1.05:
                estatus = "Estabilidad Moderada"
                colchon_meses = "3 a 5 meses"
                color_hex = "#D99B26" # Dorado
            else:
                estatus = "Volatilidad Elevada"
                colchon_meses = "6 meses o más"
                color_hex = "#DC2626" # Rojo
                
            profiles.append({
                "sector": sec,
                "grupo_edad": age,
                "n_muestra": n_sub,
                "ingreso_medio": round(m_ind, 0),
                "mediana": round(p50, 0),
                "p25": round(p25, 0),
                "p75": round(p75, 0),
                "cv_ponderado": round(cv_ind, 4),
                "ingreso_medio_asalariado": round(m_as, 0),
                "brecha_pct": round(brecha, 1),
                "estatus_estabilidad": estatus,
                "colchon_recomendado": colchon_meses,
                "color_hex": color_hex
            })
            
    profiles_json_path = os.path.join(PROCESSED_DIR, "metricas_perfiles_simulador.json")
    with open(profiles_json_path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)
    print(f"Guardado JSON de perfiles de simulador en: {profiles_json_path} ({len(profiles)} perfiles)")
    
    # También generar copia en web/js/data_store.js para consumo directo sin requerir servidor backend
    data_store_js = os.path.join(WEB_JS_DIR, "data_store.js")
    js_content = f"// Datos consolidados para el Simulador Ciudadano del Proyecto 3\nconst SIMULATOR_PROFILES = {json.dumps(profiles, ensure_ascii=False, indent=2)};\n\nconst DEPT_METRICS = {json.dumps(dept_metrics, ensure_ascii=False, indent=2)};\n"
    with open(data_store_js, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Exportado data_store.js para la Web App en: {data_store_js}")
    
    print("\n✓ PIPELINE DE DATOS EJECUTADO EXITOSAMENTE.")

if __name__ == "__main__":
    generate_datasets_and_metrics()

