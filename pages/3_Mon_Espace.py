import streamlit as st
from i18n import t, init_lang
from common import apply_base_style, render_sidebar
import db

st.set_page_config(page_title="Mon espace — SCSM Group · Lab_Math", page_icon="🔐", layout="wide")
init_lang()
apply_base_style()
render_sidebar()
db.init_db()

st.title(t("space_title"))
st.write(t("space_intro"))

email = st.text_input(t("space_email_input"))
check = st.button(t("space_check_button"), type="primary")

if check and email:
    reg = db.get_registration(email)
    if reg is None:
        st.warning(t("space_not_found"))
    elif not reg["unlocked"]:
        st.info(t("space_locked"))
    else:
        st.success(f"{t('space_unlocked_title')} — {reg['full_name']}")
        st.write("")

        modules = [
            (t("module_1_title"), t("module_1_content"), t("module_1_software")),
            (t("module_2_title"), t("module_2_content"), t("module_2_software")),
            (t("module_3_title"), t("module_3_content"), t("module_3_software")),
        ]
        for i, (title, content, software) in enumerate(modules, start=1):
            with st.expander(f"📦 {title}", expanded=(i == 1)):
                st.markdown(f"**{t('content_col')} :** {content}")
                st.markdown(f"**{t('software_col')} :** {software}")
                st.progress(0, text=t("space_module_progress"))
                st.caption(
                    "Les ressources (vidéos, PDF, sandbox R/Python, quiz) seront publiées ici par "
                    "l'administrateur au fur et à mesure de la formation."
                    if st.session_state["lang"] == "fr"
                    else "Resources (videos, PDFs, R/Python sandbox, quizzes) will be published "
                    "here by the administrator as the training progresses."
                )
