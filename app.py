import streamlit as st
from i18n import t, init_lang
from common import apply_base_style, render_sidebar, render_logo_slot

st.set_page_config(
    page_title="SCSM Group · Lab_Math — Formation Santé Publique",
    page_icon="📊",
    layout="wide",
)

init_lang()
apply_base_style()
render_sidebar()

# ---------------- HERO ----------------
st.markdown(
    f"""
    <div class="scsm-hero">
        <span class="scsm-tag">{t('special_training')}</span>
        <h1>{t('training_title')}</h1>
        <h3 style="color:#dbe9ff;font-weight:400;">{t('training_subtitle')}</h3>
        <p style="margin-top:0.8rem;">{t('organized_by')}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

logo_col1, logo_col2, cta_col = st.columns([1, 1, 2])
with logo_col1:
    render_logo_slot("logo_scsm_path", "logo_scsm_caption", height=70)
with logo_col2:
    render_logo_slot("logo_labmath_path", "logo_labmath_caption", height=70)
with cta_col:
    st.write("")
    b1, b2 = st.columns(2)
    with b1:
        if st.button(t("cta_enroll"), type="primary", use_container_width=True):
            st.switch_page("pages/2_Paiement_Inscription.py")
    with b2:
        if st.button(t("cta_program"), use_container_width=True):
            st.switch_page("pages/1_Programme.py")

st.write("")

# ---------------- ABOUT ----------------
st.subheader(t("about_us_title"))
st.markdown(t("about_us_text"))

st.write("")

# ---------------- OBJECTIVES ----------------
st.subheader(t("objectives_title"))
o1, o2 = st.columns(2)
with o1:
    st.markdown(f"- {t('objective_1')}")
    st.markdown(f"- {t('objective_2')}")
with o2:
    st.markdown(f"- {t('objective_3')}")
    st.markdown(f"- {t('objective_4')}")

st.write("")

# ---------------- WHY US ----------------
st.subheader(t("why_us_title"))
w1, w2, w3, w4, w5 = st.columns(5)
for col, key in zip([w1, w2, w3, w4, w5], ["why_1", "why_2", "why_3", "why_4", "why_5"]):
    with col:
        st.markdown(f"<div class='scsm-card'>{t(key)}</div>", unsafe_allow_html=True)

st.write("")

# ---------------- LOCATIONS ----------------
loc_col, contact_col = st.columns([2, 1])
with loc_col:
    st.subheader(t("locations_title"))
    st.markdown(t("locations_text"))
with contact_col:
    st.subheader(t("contact_title"))
    st.markdown(
        "📞 674 65 18 56 / 691 13 32 53\n\n"
        "📞 678 07 18 81 / 663 43 34 87 / 692 52 81 36\n\n"
        "✉️ scsmaubma@gmail.com\n\n"
        "🌐 scsmaubmar.org\n\n"
        "Lab_Math : labmathscsmaubmarorg.netlify.app"
    )

st.divider()
st.caption("SCSM Group — Statistic Consulting Survey and Multiservices · Votre satisfaction, notre plaisir, au service de l'humanité.")
