import streamlit as st

st.set_page_config(page_title="Simulador PTAR Panamá - Ecoeficiente", layout="centered")

st.title("🌐 Simulador de Tratamiento de Aguas Residuales")
st.caption("Adaptado al marco normativo de la República de Panamá (DGNTI-COPANIT)")

# --- BLOQUE 1: INPUTS ---
st.header("📥 1. Parámetros de Entrada")

col1, col2 = st.columns(2)
with col1:
    p_i = st.number_input("Población Actual (hab):", min_value=100, value=2800, step=100)
    t = st.number_input("Período de Diseño (años):", min_value=1, max_value=40, value=20)
    
with col2:
    zona = st.selectbox("Tipo de Zona (Tasa de Crecimiento):", 
                        ["Urbana / Expansión (2.2%)", "Promedio Nacional (1.35%)", "Rural Estable (1.1%)"])
    dotacion_tipo = st.selectbox("Entorno / Dotación de Agua:", 
                                 ["Urbana Estándar - IDAAN (400 L/hab·día)", "Rural / Consumo Bajo (250 L/hab·día)"])

c_retorno = st.slider("Coeficiente de Retorno:", min_value=0.70, max_value=0.85, value=0.80, step=0.05)
destino = st.radio("Destino Final del Efluente Tratado:", 
                   ["Cuerpo de agua natural (Río/Quebrada)", "Red de Alcantarillado Sanitario", "Reúso en Riego Agrícola"])

# Mapeo de parámetros seleccionados
r = 0.022 if "Urbana" in zona else (0.0135 if "Nacional" in zona else 0.011)
dotacion = 400 if "IDAAN" in dotacion_tipo else 250
factor_pico = 2.5 if dotacion == 400 else 2.8

# --- BLOQUE 2: PROCESAMIENTO ---
if st.button("🚀 Calcular Dimensionamiento Ecoeficiente"):
    # 1. Población Futura
    p_f = int(p_i * ((1 + r) ** t))
    
    # 2. Caudales
    q_medio_dia = (p_f * dotacion * c_retorno)
    q_medio_l_s = q_medio_dia / 86400
    q_medio_m3_dia = q_medio_l_s * 86.4
    q_max_horario = q_medio_l_s * factor_pico
    
    # 3. Carga Orgánica
    carga_dbo = (p_f * 50) / 1000  # g/hab/dia a kg/dia
    concentracion_dbo = (carga_dbo / q_medio_m3_dia) * 1000

    # --- BLOQUE 3: OUTPUTS ---
    st.header("📊 2. Resultados del Diseño")
    
    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.metric("Población Futura de Diseño ($P_f$)", f"{p_f} hab")
        st.metric("Caudal Medio Diario ($Q_{medio}$)", f"{q_medio_l_s:.2f} L/s", f"{q_medio_m3_dia:.1f} m³/día")
    with metrics_col2:
        st.metric("Caudal Máximo Horario ($Q_{máx}$)", f"{q_max_horario:.2f} L/s")
        st.metric("Carga Orgánica de Diseño", f"{carga_dbo:.1f} kg DBO/día", f"Conc. Real: {concentracion_dbo:.1f} mg/L")

    st.header("🛡️ 3. Evaluación de Ecoeficiencia y Cumplimiento Legal")
    
    # Evaluación Normativa Dinámica
    if "Cuerpo de agua" in destino:
        st.error("⚠️ Cumplimiento Legal Requerido: COPANIT 35-2019\n\nEl efluente se verterá en una masa hídrica natural. Se exigen límites de vertido sumamente estrictos (DBO < 30 mg/L). Se sugiere una combinación de reactor UASB complementado con humedales de pulido o lagunas facultativas.")
    elif "Alcantarillado" in destino:
        st.info("📝 Cumplimiento Legal Requerido: COPANIT 39-2023\n\nEl agua residual va directo a recolección municipal. Los parámetros se concentran en mitigar sólidos gruesos, aceites y pH corrosivos para no dañar las líneas del alcantarillado público.")
    else:
        st.success("🌾 Cumplimiento Legal Requerido: COPANIT 24-99 (Economía Circular)\n\n¡Excelente enfoque! El destino es el reúso directo agrícola. La norma exige estrictas restricciones sanitarias en coliformes fecales y huevos de helmintos. Requiere la integración mandatoria de lagunas de maduración o sistemas de desinfección UV/Cloración.")
        
    st.markdown("ℹ️ *Nota del Lodo:* Todo lodo extraído de los reactores debe ser estabilizado mediante lechos de secado y evaluado rigurosamente bajo la norma **COPANIT 47** previo a cualquier aprovechamiento agrícola.")
