import streamlit as st
import pandas as pd
from i18n import t, init_lang
from common import apply_base_style, render_sidebar

st.set_page_config(page_title="Programme — SCSM Group · Lab_Math", page_icon="📋", layout="wide")
init_lang()
apply_base_style()
render_sidebar()

st.title(t("program_title"))

df = pd.DataFrame(
    {
        t("module_col"): [t("module_1_title"), t("module_2_title"), t("module_3_title")],
        t("content_col"): [t("module_1_content"), t("module_2_content"), t("module_3_content")],
        t("software_col"): [t("module_1_software"), t("module_2_software"), t("module_3_software")],
    }
)
st.table(df)

st.write("")
st.subheader(t("target_audience_title"))
for key in ["audience_1", "audience_2", "audience_3", "audience_4", "audience_5"]:
    st.markdown(f"- {t(key)}")

st.write("")
st.subheader(t("services_title"))
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='scsm-card'>{t('service_scsm')}</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='scsm-card'>{t('service_labmath')}</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='scsm-card'>{t('service_multi')}</div>", unsafe_allow_html=True)

st.write("")
if st.button(t("cta_enroll"), type="primary"):
    st.switch_page("pages/2_Paiement_Inscription.py")
