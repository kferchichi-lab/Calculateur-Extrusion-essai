import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Calculateur Extrusion TPR", 
    page_icon="📟", 
    layout="wide",
    initial_sidebar_state="auto"
)

# --- CSS CORRECTIF (Sidebar + Marges) ---
st.markdown("""
    <style>
        /* Réactivation de la visibilité du bouton Sidebar */
        [data-testid="stSidebarNav"] {padding-top: 2rem;}
        
        /* Ajustement du Header Streamlit pour laisser apparaître la flèche (>) */
        header {
            visibility: visible !important;
            height: 50px !important;
            background-color: transparent !important;
        }

        /* Marges pour éviter le 'Crop' sur PC et Mobile */
        .block-container {
            padding-top: 1rem !important; 
            padding-bottom: 2rem !important;
            padding-left: 5rem !important;
            padding-right: 5rem !important;
        }

        /* Adaptabilité Smartphone */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1.5rem !important;
                padding-right: 1.5rem !important;
                padding-top: 0.5rem !important;
            }
            /* On s'assure que le titre ne touche pas les bords */
            h2 { font-size: 1.4rem !important; }
        }

        /* Correction du logo */
        [data-testid="stImage"] img {
            max-width: 100%;
            height: auto;
            object-fit: contain !important;
        }

        /* Style des barres de résultat */
        .container-barre { width: 100%; background-color: #e0e0e0; border-radius: 5px; height: 22px; position: relative;}
        .barre-lopin { background-color: #808080; height: 100%; border-radius: 5px; transition: width 0.5s;}
        .barre-limite { background-color: #1a4332; height: 8px; border-radius: 5px; margin-top: 4px;}
        
        /* Style Bouton Calculer */
        div.stButton > button {
            width: 100%; 
            font-weight: bold; 
            background-color: #0047AB; 
            color: white; 
            height: 3.5em; 
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION TECHNIQUE ---
CONFIG_PRESSES = {
    "Presse 4": {"diametre": 228, "limite_longueur": 1100},
    "Presse 6": {"diametre": 178, "limite_longueur": 890},
    "Presse 7": {"diametre": 178, "limite_longueur": 1000},
}

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    presse_choisie = st.selectbox(
        "Sélectionnez la Presse :",
        options=list(CONFIG_PRESSES.keys()),
        index=None,
        placeholder="Choisir..."
    )
    if presse_choisie:
        st.success(f"Presse active : {presse_choisie}")
    else:
        st.info("Sélectionnez une presse pour voir ses limites.")

# --- EN-TÊTE ---
col_logo, col_titre = st.columns([1, 4])
with col_logo:
    st.image("https://scontent.fnbe1-2.fna.fbcdn.net/v/t39.30808-6/408929007_749166663924252_578772537697061170_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=1d70fc&_nc_ohc=outSX1TrNzMQ7kNvwH8dLos&_nc_oc=AdnayidTjVde0oO8dBewwk-Vo1bwbpm9MvDcBijNWzBt6b_52O9jssFyIDcLrqtW-bk&_nc_zt=23&_nc_ht=scontent.fnbe1-2.fna&_nc_gid=mw-_AZkaw4Oh_IX1S6ObVQ&oh=00_AfuIu1RSs4hY2piAZBZvukecG5Pl97xctCOBml-nIqgrIQ&oe=69A62B8A", width=120)

with col_titre:
    st.markdown("<h2 style='margin: 0;'>Tunisie Profilés d'Aluminium</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin: 0; color: #555; font-weight: normal;'>Direction Maintenance et Travaux Neufs</h4>", unsafe_allow_html=True)

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# --- VÉRIFICATION SÉLECTION ---
if not presse_choisie:
    st.warning("👈 **Ouvrez le menu à gauche** (flèche >) pour choisir une presse.")
    st.stop()

st.subheader(f"📟 Calculateur - {presse_choisie}")

# --- INPUTS ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    type_billette = st.selectbox("Nature billette :", ["Primaire", "Recyclée"])
    p_m = st.number_input("P/m (kg/m)", value=None, format="%.3f")
with col_in2:
    n_ecoulements = st.number_input("Écoulements", min_value=1, step=1)
    long_demandee = st.number_input("Longueur demandée (m)", value=None, format="%.2f")

# --- CALCULS ---
if st.button("🧮 CALCULER"):
    if p_m and long_demandee:
        limite_max = CONFIG_PRESSES[presse_choisie]["limite_longueur"]
        diam = CONFIG_PRESSES[presse_choisie]["diametre"]
        
        k = 0.1 if type_billette == "Primaire" else 0.16
        long_culot_mm = k * diam
        poids_lopin = ((p_m * n_ecoulements) * long_demandee) + (110.180 * (long_culot_mm / 1000))
        long_lopin_mm = (poids_lopin / 110.180) * 1000

        if long_lopin_mm > limite_max:
            st.error(f"🚨 Valeurs non valides pour la {presse_choisie}")
            st.markdown(f"**Lopin : {long_lopin_mm:.2f} mm** | Limite : {limite_max} mm")
        else:
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("📏 CULOT (mm)", f"{long_culot_mm:.2f}")
                st.metric("🎯 LOPIN (mm)", f"{long_lopin_mm:.2f}")
            with res_col2:
                st.metric("⚖️ POIDS (kg)", f"{poids_lopin:.3f}")
                pourcent = min((long_lopin_mm / limite_max) * 100, 100)
                st.write(f"📊 Charge : {long_lopin_mm:.0f} / {limite_max} mm")
                st.markdown(f'<div class="container-barre"><div class="barre-lopin" style="width: {pourcent}%;"></div></div>', unsafe_allow_html=True)
                st.markdown('<div class="barre-limite" style="width: 100%;"></div>', unsafe_allow_html=True)
            st.success("✅ Dimensions validées.")

# --- FOOTER ---
st.markdown("<br><div style='text-align: center; color: gray; font-size: 0.8rem;'>© 2026 TPR - Maintenance</div>", unsafe_allow_html=True)
