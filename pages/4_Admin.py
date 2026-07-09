import os
import streamlit as st
from i18n import t, init_lang
from common import apply_base_style, render_sidebar, LOGO_DIR
import db

st.set_page_config(page_title="Admin — SCSM Group · Lab_Math", page_icon="🛠️", layout="wide")
init_lang()
apply_base_style()
render_sidebar()
db.init_db()

# Mot de passe : variable d'environnement ADMIN_PASSWORD, ou secrets.toml, avec repli de démo.
ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD", st.secrets.get("ADMIN_PASSWORD", "changeme123") if hasattr(st, "secrets") else "changeme123"
)

st.title(t("admin_title"))

if "admin_authed" not in st.session_state:
    st.session_state["admin_authed"] = False

if not st.session_state["admin_authed"]:
    pwd = st.text_input(t("admin_password_label"), type="password")
    if st.button(t("admin_login_button"), type="primary"):
        if pwd == ADMIN_PASSWORD:
            st.session_state["admin_authed"] = True
            st.rerun()
        else:
            st.error(t("admin_wrong_password"))
    st.stop()

# ---- Authenticated admin view ----
top_l, top_r = st.columns([4, 1])
with top_r:
    if st.button(t("admin_logout")):
        st.session_state["admin_authed"] = False
        st.rerun()

st.divider()

# --- Unlock a learner (email only, as requested) ---
st.subheader(t("admin_unlock_title"))
st.write(t("admin_unlock_text"))
unlock_col1, unlock_col2 = st.columns([3, 1])
with unlock_col1:
    unlock_email = st.text_input(t("admin_unlock_email_input"), key="unlock_email_input")
with unlock_col2:
    st.write("")
    st.write("")
    if st.button(t("admin_unlock_button"), type="primary", use_container_width=True):
        if unlock_email:
            existing = db.get_registration(unlock_email)
            if existing is None:
                # L'admin peut débloquer même sans déclaration préalable (ex: dépôt bancaire traité hors-ligne)
                db.add_registration(unlock_email, "", "", "Admin", "", "")
            db.set_unlocked(unlock_email, True)
            st.success(f"{t('admin_unlock_success')} {unlock_email}")
            st.rerun()

st.divider()

# --- Registrations table ---
st.subheader(t("admin_pending_title"))
rows = db.list_registrations()
if not rows:
    st.info(t("admin_no_pending"))
else:
    for r in rows:
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.markdown(f"**{r['email']}**  \n{r['full_name'] or ''}  ·  {r['phone'] or ''}")
                st.caption(f"{r['method'] or ''} — Ref: {r['reference'] or '—'} — {r['amount'] or ''}")
            with c2:
                st.caption(f"{'🟢 ' + t('status_unlocked') if r['unlocked'] else '🟡 ' + t('status_pending')}")
                st.caption(f"{r['created_at'] or ''}")
            with c3:
                if r["unlocked"]:
                    if st.button(t("admin_lock_button"), key=f"lock_{r['email']}"):
                        db.set_unlocked(r["email"], False)
                        st.rerun()
                else:
                    if st.button(t("admin_unlock_button"), key=f"unlock_{r['email']}"):
                        db.set_unlocked(r["email"], True)
                        st.rerun()

st.divider()

# --- Logo management ---
st.subheader(t("admin_logos_title"))
lc1, lc2 = st.columns(2)
with lc1:
    scsm_file = st.file_uploader(t("admin_upload_scsm"), type=["png", "jpg", "jpeg", "svg"], key="scsm_logo")
    if scsm_file is not None:
        path = os.path.join(LOGO_DIR, "logo_scsm" + os.path.splitext(scsm_file.name)[1])
        with open(path, "wb") as f:
            f.write(scsm_file.getbuffer())
        db.set_setting("logo_scsm_path", path)
        st.success("✅")
    current = db.get_setting("logo_scsm_path")
    if current and os.path.exists(current):
        st.image(current, width=160)

with lc2:
    labmath_file = st.file_uploader(t("admin_upload_labmath"), type=["png", "jpg", "jpeg", "svg"], key="labmath_logo")
    if labmath_file is not None:
        path = os.path.join(LOGO_DIR, "logo_labmath" + os.path.splitext(labmath_file.name)[1])
        with open(path, "wb") as f:
            f.write(labmath_file.getbuffer())
        db.set_setting("logo_labmath_path", path)
        st.success("✅")
    current = db.get_setting("logo_labmath_path")
    if current and os.path.exists(current):
        st.image(current, width=160)
