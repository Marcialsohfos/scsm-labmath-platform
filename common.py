import os
import streamlit as st
from i18n import t, init_lang, toggle_lang
import db

LOGO_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(LOGO_DIR, exist_ok=True)

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
