import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Calculateur Extrusion", page_icon="📟", layout="wide")

# CSS pour le style et les barres
st.markdown("""
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        .container-barre { width: 100%; background-color: #e0e0e0; border-radius: 5px; margin-bottom: 10px; position: relative; height: 25px;}
        .barre-lopin { background-color: #808080; height: 100%; border-radius: 5px; transition: width 0.5s;}
        .barre-limite { background-color: #006400; height: 8px; border-radius: 2px; margin-top: 5px;}
        .label-barre { font-size: 0.8em; color: #555; margin-bottom: 2px;}
    </style>
    """, unsafe_allow_html=True)

# --- EN-TÊTE ---
col_logo, col_titre = st.columns([1, 5])
with col_logo:
    st.write("🏢") 
with col_titre:
    st.markdown("### NOM DE VOTRE SOCIÉTÉ | <span style='color:gray'>Assistant Extrusion</span>", unsafe_allow_html=True)

# --- SAISIE ---
st.markdown("##### 📥 Paramètres d'entrée")
c1, c2, c3, c4 = st.columns(4)
with c1:
    type_billette = st.selectbox("Billette", ["Primaire", "Recyclée"])
with c2:
    p_m = st.number_input("P/m (kg/m)", value=None, format="%.3f", placeholder="0.000")
with c3:
    n_ecoulements = st.number_input("Écoulements", min_value=1, step=1)
with c4:
    long_demandee = st.number_input("Long. (m)", value=None, format="%.2f", placeholder="0.00")

if st.button("🧮 CALCULER"):
    if p_m is not None and long_demandee is not None:
        # CALCULS
        k = 0.1 if type_billette == "Primaire" else 0.16
        long_culot_mm = k * 228
        poids_lineique_billette = 110.180
        poids_lopin = ((p_m * n_ecoulements) * long_demandee) + (poids_lineique_billette * (long_culot_mm / 1000))
        long_lopin_mm = (poids_lopin / poids_lineique_billette) * 1000
        
        # LIMITE MACHINE
        LIMITE_MAX = 1100.0
        # Calcul du pourcentage pour l'affichage (max 100%)
        pourcentage_lopin = min((long_lopin_mm / LIMITE_MAX) * 100, 100)
        
        if long_lopin_mm > LIMITE_MAX:
            st.error(f"⚠️ TROP LONG : {long_lopin_mm:.2f} mm (Limite {LIMITE_MAX} mm dépassée)")
        else:
            st.markdown("---")
            col_val, col_visu = st.columns([1, 2])
            
            with col_val:
                st.metric("🎯 LONGUEUR LOPIN", f"{long_lopin_mm:.2f} mm")
                st.metric("📏 CULOT", f"{long_culot_mm:.2f} mm")
                st.metric("⚖️ POIDS", f"{poids_lopin:.3f} kg")

            with col_visu:
                st.markdown("<br>", unsafe_allow_html=True)
                # Barre Grise (Lopin actuel)
                st.markdown(f'<div class="label-barre">Lopin actuel : {long_lopin_mm:.2f} mm</div>', unsafe_allow_html=True)
                st.markdown(f'''
                    <div class="container-barre">
                        <div class="barre-lopin" style="width: {pourcentage_lopin}%;"></div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # Barre Vert Sombre (Limite Cisaille)
                st.markdown(f'<div class="label-barre">Capacité Tapis Cisaille (Limite : {LIMITE_MAX} mm)</div>', unsafe_allow_html=True)
                st.markdown('<div class="barre-limite" style="width: 100%;"></div>', unsafe_allow_html=True)
                
                st.success("✅ Dimension conforme à la capacité machine.")
    else:
        st.warning("⚠️ Veuillez remplir les champs.")

# PIED DE PAGE
st.markdown(f'<div style="position: fixed; bottom: 10px; width:100%; text-align: center; color: gray; font-size: 0.8em;">© 2026 NOM DE VOTRE SOCIÉTÉ</div>', unsafe_allow_html=True)
