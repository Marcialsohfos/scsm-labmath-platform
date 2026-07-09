import streamlit as st
from i18n import t, init_lang
from common import apply_base_style, render_sidebar
import db

st.set_page_config(page_title="Paiement & Inscription — SCSM Group · Lab_Math", page_icon="💳", layout="wide")
init_lang()
apply_base_style()
render_sidebar()
db.init_db()

st.title(t("payment_title"))
st.write(t("payment_intro"))

col_local, col_intl = st.columns(2)

with col_local:
    st.markdown(f"### {t('local_payment_title')}")
    st.markdown(
        f"""
        <div class="payment-box">
        <b>{t('momo_label')} (MTN)</b><br>
        📱 674 65 18 56<br>
        📱 691 13 32 53<br><br>
        <b>{t('om_label')} (Orange)</b><br>
        📱 678 07 18 81<br>
        📱 663 43 34 87<br>
        📱 692 52 81 36
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_intl:
    st.markdown(f"### {t('intl_payment_title')}")
    st.markdown(f"<div class='payment-box'>{t('intl_payment_text')}</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown(f"### {t('bank_deposit_title')}")
    st.markdown(f"<div class='payment-box'>{t('bank_deposit_text')}</div>", unsafe_allow_html=True)
    st.link_button(t("contact_admin_button"), "mailto:scsmaubma@gmail.com", use_container_width=True)

st.divider()

st.subheader(t("declare_payment_title"))
st.write(t("declare_payment_text"))

with st.form("payment_declaration", clear_on_submit=True):
    full_name = st.text_input(t("form_fullname"))
    email = st.text_input(t("form_email"))
    phone = st.text_input(t("form_phone"))
    method = st.selectbox(
        t("form_method"),
        ["MTN MoMo", "Orange Money", "Carte bancaire / Bank card", "Dépôt bancaire / Bank deposit"],
    )
    reference = st.text_input(t("form_ref"))
    amount = st.text_input(t("form_amount"))
    submitted = st.form_submit_button(t("form_submit"), type="primary")

    if submitted:
        if not full_name or not email:
            st.error(t("form_missing"))
        else:
            db.add_registration(email, full_name, phone, method, reference, amount)
            st.success(t("form_success"))
