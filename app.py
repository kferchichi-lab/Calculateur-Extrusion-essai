import streamlit as st

# Configuration de la page pour utiliser toute la largeur et masquer le menu
st.set_page_config(page_title="Calculateur Extrusion", page_icon="📟", layout="wide")

# CSS pour supprimer les marges blanches en haut de page
st.markdown("""
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        div.stButton > button {width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white;}
    </style>
    """, unsafe_allow_html=True)

# --- EN-TÊTE COMPACT ---
col_logo, col_titre = st.columns([1, 5])
with col_logo:
    st.write("🏢") 
with col_titre:
    st.markdown("### NOM DE VOTRE SOCIÉTÉ | <span style='color:gray'>Assistant Extrusion</span>", unsafe_allow_html=True)

# --- SECTION 1 : SAISIE (Sur une seule ligne pour gagner de la place) ---
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

# --- BOUTON DE CALCUL ---
if st.button("🧮 CALCULER"):
    if p_m is not None and long_demandee is not None:
        # CALCULS
        k = 0.1 if type_billette == "Primaire" else 0.16
        long_culot_mm = k * 228
        poids_lineique_billette = 110.180
        poids_lopin = ((p_m * n_ecoulements) * long_demandee) + (poids_lineique_billette * (long_culot_mm / 1000))
        long_lopin_mm = (poids_lopin / poids_lineique_billette) * 1000
        
        # VÉRIFICATION 1100 mm
        if long_lopin_mm > 1100:
            st.markdown(f"""
                <div style="background-color: #ff4b4b; padding: 15px; border-radius: 10px; text-align: center; color: white;">
                    <h3 style="margin:0;">⚠️ TROP LONG : {long_lopin_mm:.2f} mm</h3>
                    <p style="margin:0;">La limite est de 1100 mm.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # AFFICHAGE COMPACT DES RÉSULTATS (Sur une seule ligne)
            st.markdown("##### 📋 Résultats de réglage")
            res1, res2, res3 = st.columns(3)
            
            res1.metric("📏 CULOT (mm)", f"{long_culot_mm:.2f}")
            res2.metric("⚖️ POIDS (kg)", f"{poids_lopin:.3f}")
            res3.metric("🎯 LOPIN (mm)", f"{long_lopin_mm:.2f}")
            
            st.success("✅ Réglages validés.")
    else:
        st.warning("⚠️ Remplissez toutes les cases.")

# --- PIED DE PAGE ---
st.markdown(
    """
    <div style="position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; color: gray; font-size: 0.8em;">
        © 2026 <b>NOM DE VOTRE SOCIÉTÉ</b>
    </div>
    """, 
    unsafe_allow_html=True
)
