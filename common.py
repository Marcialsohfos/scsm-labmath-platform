import os
import streamlit as st
from i18n import t, init_lang, toggle_lang
import db

LOGO_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(LOGO_DIR, exist_ok=True)

MODULE_FILES_DIR = os.path.join(os.path.dirname(__file__), "data", "module_files")
os.makedirs(MODULE_FILES_DIR, exist_ok=True)

# Garantit que les tables SQLite existent dès que ce module est importé,
# quelle que soit la page (corrige "no such table: settings" sur un
# déploiement neuf, ex. Streamlit Cloud).
db.init_db()

PRIMARY = "#0B5FA5"   # bleu SCSM
ACCENT = "#F2A900"    # or / jaune Lab_Math


def apply_base_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(180deg, #f7fafc 0%, #ffffff 35%);
        }}
        h1, h2, h3 {{
            color: {PRIMARY};
        }}
        .scsm-hero {{
            background: linear-gradient(120deg, {PRIMARY} 0%, #063a66 100%);
            color: white;
            padding: 2.2rem 2rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
        }}
        .scsm-hero h1 {{
            color: white !important;
            margin-bottom: 0.2rem;
        }}
        .scsm-tag {{
            display:inline-block;
            background: {ACCENT};
            color: #1a1a1a;
            font-weight: 700;
            padding: 0.25rem 0.8rem;
            border-radius: 999px;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
            margin-bottom: 0.6rem;
        }}
        .scsm-card {{
            background: white;
            border: 1px solid #e6eaf0;
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 2px 10px rgba(20,30,60,0.04);
            height: 100%;
        }}
        .payment-box {{
            border: 1px dashed {PRIMARY};
            border-radius: 14px;
            padding: 1rem 1.2rem;
            background: #f5f9ff;
        }}

        /* ---------- Animations ---------- */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(16px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to   {{ opacity: 1; }}
        }}
        @keyframes gradientShift {{
            0%   {{ background-position: 0% 50%; }}
            50%  {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes pulseBadge {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(242,169,0,0.55); }}
            50% {{ box-shadow: 0 0 0 8px rgba(242,169,0,0); }}
        }}
        @keyframes shimmer {{
            0% {{ background-position: -400px 0; }}
            100% {{ background-position: 400px 0; }}
        }}

        .stApp {{
            animation: fadeIn 0.5s ease-in;
        }}

        .scsm-hero {{
            background-size: 220% 220%;
            animation: gradientShift 10s ease infinite, fadeInUp 0.6s ease-out;
        }}

        .scsm-tag {{
            animation: pulseBadge 2.2s infinite;
        }}

        .scsm-card {{
            animation: fadeInUp 0.5s ease-out both;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }}
        .scsm-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 24px rgba(20,30,60,0.10);
        }}

        .scsm-module-card {{
            animation: fadeInUp 0.45s ease-out both;
            border-left: 4px solid {ACCENT};
            transition: border-color 0.2s ease, transform 0.2s ease;
        }}
        .scsm-module-card:hover {{
            border-left-color: {PRIMARY};
        }}

        .scsm-resource-row {{
            animation: fadeIn 0.4s ease-out both;
        }}

        div.stButton > button, div.stDownloadButton > button {{
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        div.stButton > button:hover, div.stDownloadButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(11,95,165,0.18);
        }}

        div[data-testid="stExpander"] {{
            animation: fadeInUp 0.4s ease-out both;
            transition: box-shadow 0.2s ease;
        }}

        .stProgress > div > div > div > div {{
            transition: width 0.6s ease;
            background-image: linear-gradient(90deg, {PRIMARY}, {ACCENT});
        }}

        .scsm-done-badge {{
            display:inline-block;
            background: #1fa956;
            color: white;
            font-weight: 700;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            font-size: 0.72rem;
            animation: fadeIn 0.4s ease-out;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo_slot(setting_key, caption_key, upload_key=None, height=90):
    """Displays the uploaded logo if available, otherwise a placeholder hint."""
    path = db.get_setting(setting_key)
    if path and os.path.exists(path):
        st.image(path, caption=t(caption_key), width=height * 2)
    else:
        st.markdown(
            f"""
            <div style="border:2px dashed #c9d4e3;border-radius:12px;
                        height:{height}px;display:flex;align-items:center;
                        justify-content:center;color:#8a97ab;font-size:0.85rem;
                        text-align:center;padding:0.5rem;">
                {t('logo_upload_hint')}
            </div>
            """,
            unsafe_allow_html=True,
        )


RESOURCE_ICONS = {
    "video": "🎬",
    "text": "📖",
    "pdf": "📑",
    "sandbox": "💻",
    "quiz": "❓",
}


def module_title(module):
    lang = st.session_state.get("lang", "fr")
    if lang == "en" and module["title_en"]:
        return module["title_en"]
    return module["title_fr"]


def module_description(module):
    lang = st.session_state.get("lang", "fr")
    if lang == "en" and module["description_en"]:
        return module["description_en"]
    return module["description_fr"] or ""


def render_sidebar():
    init_lang()
    with st.sidebar:
        st.markdown("### SCSM Group · Lab_Math")
        col1, col2 = st.columns(2)
        with col1:
            render_logo_slot("logo_scsm_path", "logo_scsm_caption", height=45)
        with col2:
            render_logo_slot("logo_labmath_path", "logo_labmath_caption", height=45)

        st.button(t("lang_button_label"), on_click=toggle_lang, use_container_width=True)
        st.divider()
        st.page_link("app.py", label=t("nav_home"), icon="🏠")
        st.page_link("pages/1_Programme.py", label=t("nav_program"), icon="📋")
        st.page_link("pages/2_Paiement_Inscription.py", label=t("nav_payment"), icon="💳")
        st.page_link("pages/3_Mon_Espace.py", label=t("nav_space"), icon="🔐")
        st.page_link("pages/4_Admin.py", label=t("nav_admin"), icon="🛠️")
        st.divider()
        st.caption("📞 674 65 18 56 / 691 13 32 53")
        st.caption("📞 678 07 18 81 / 663 43 34 87")
        st.caption("✉️ scsmaubma@gmail.com")
        st.caption("🌐 scsmaubmar.org")
