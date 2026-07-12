import os
import json
import streamlit as st
from i18n import t, init_lang
from common import apply_base_style, render_sidebar, LOGO_DIR, MODULE_FILES_DIR, module_title, RESOURCE_ICONS
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

st.divider()

# ==================================================================
# --- Gestion des modules et de leur contenu pédagogique ---
# ==================================================================
st.subheader(t("admin_modules_title"))
st.caption(t("admin_modules_help"))

with st.expander(t("admin_add_module"), expanded=False):
    with st.form("add_module_form", clear_on_submit=True):
        mc1, mc2 = st.columns(2)
        with mc1:
            new_title_fr = st.text_input(t("module_title_fr"))
            new_desc_fr = st.text_area(t("module_desc_fr"))
        with mc2:
            new_title_en = st.text_input(t("module_title_en"))
            new_desc_en = st.text_area(t("module_desc_en"))
        if st.form_submit_button(t("admin_add_module_button"), type="primary"):
            if new_title_fr.strip():
                db.add_module(new_title_fr.strip(), new_title_en.strip(), new_desc_fr, new_desc_en)
                st.success(t("admin_module_added"))
                st.rerun()
            else:
                st.warning(t("module_title_required"))

modules = db.list_modules()
if not modules:
    st.info(t("admin_no_modules"))

for i, m in enumerate(modules):
    with st.container(border=True):
        header_col, up_col, down_col, del_col = st.columns([6, 1, 1, 1])
        with header_col:
            st.markdown(f"### 📦 {module_title(m)}")
        with up_col:
            if st.button("⬆️", key=f"up_{m['id']}", disabled=(i == 0), use_container_width=True):
                db.move_module(m["id"], -1)
                st.rerun()
        with down_col:
            if st.button("⬇️", key=f"down_{m['id']}", disabled=(i == len(modules) - 1), use_container_width=True):
                db.move_module(m["id"], 1)
                st.rerun()
        with del_col:
            if st.button("🗑️", key=f"delmod_{m['id']}", use_container_width=True):
                db.delete_module(m["id"])
                st.rerun()

        with st.expander(t("admin_edit_module")):
            with st.form(f"edit_module_form_{m['id']}"):
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_title_fr = st.text_input(t("module_title_fr"), value=m["title_fr"], key=f"efr_{m['id']}")
                    e_desc_fr = st.text_area(t("module_desc_fr"), value=m["description_fr"] or "", key=f"edfr_{m['id']}")
                with ec2:
                    e_title_en = st.text_input(t("module_title_en"), value=m["title_en"] or "", key=f"een_{m['id']}")
                    e_desc_en = st.text_area(t("module_desc_en"), value=m["description_en"] or "", key=f"eden_{m['id']}")
                if st.form_submit_button(t("admin_save_changes")):
                    db.update_module(m["id"], e_title_fr, e_title_en, e_desc_fr, e_desc_en)
                    st.success("✅")
                    st.rerun()

        st.markdown(f"**{t('admin_add_content')}**")
        tabs = st.tabs([
            f"🎬 {t('resource_video')}",
            f"📖 {t('resource_text')}",
            f"📑 {t('resource_pdf')}",
            f"💻 {t('resource_sandbox')}",
            f"❓ {t('resource_quiz')}",
        ])

        # ---- Vidéo ----
        with tabs[0]:
            v_title = st.text_input(t("resource_title_label"), key=f"vt_{m['id']}")
            v_url = st.text_input(t("resource_video_url_label"), key=f"vu_{m['id']}", placeholder="https://youtube.com/...")
            v_file = st.file_uploader(t("resource_video_file_label"), type=["mp4", "webm", "mov"], key=f"vf_{m['id']}")
            if st.button(t("admin_publish"), key=f"vpub_{m['id']}", type="primary"):
                path = None
                if v_file is not None:
                    dest_dir = os.path.join(MODULE_FILES_DIR, str(m["id"]))
                    os.makedirs(dest_dir, exist_ok=True)
                    path = os.path.join(dest_dir, v_file.name)
                    with open(path, "wb") as f:
                        f.write(v_file.getbuffer())
                if not path and not v_url.strip():
                    st.warning(t("resource_video_missing"))
                else:
                    db.add_resource(m["id"], "video", v_title.strip() or t("resource_video"),
                                     file_path=path, external_url=v_url.strip() or None)
                    st.success(t("admin_content_published"))
                    st.rerun()

        # ---- Cours en texte ----
        with tabs[1]:
            tx_title = st.text_input(t("resource_title_label"), key=f"tt_{m['id']}")
            tx_content = st.text_area(t("resource_text_content_label"), height=220, key=f"tc_{m['id']}")
            if st.button(t("admin_publish"), key=f"tpub_{m['id']}", type="primary"):
                if tx_content.strip():
                    db.add_resource(m["id"], "text", tx_title.strip() or t("resource_text"), text_content=tx_content)
                    st.success(t("admin_content_published"))
                    st.rerun()
                else:
                    st.warning(t("resource_text_missing"))

        # ---- PDF ----
        with tabs[2]:
            p_title = st.text_input(t("resource_title_label"), key=f"pt_{m['id']}")
            p_file = st.file_uploader(t("resource_pdf_file_label"), type=["pdf"], key=f"pf_{m['id']}")
            if st.button(t("admin_publish"), key=f"ppub_{m['id']}", type="primary"):
                if p_file is not None:
                    dest_dir = os.path.join(MODULE_FILES_DIR, str(m["id"]))
                    os.makedirs(dest_dir, exist_ok=True)
                    path = os.path.join(dest_dir, p_file.name)
                    with open(path, "wb") as f:
                        f.write(p_file.getbuffer())
                    db.add_resource(m["id"], "pdf", p_title.strip() or p_file.name, file_path=path)
                    st.success(t("admin_content_published"))
                    st.rerun()
                else:
                    st.warning(t("resource_pdf_missing"))

        # ---- Sandbox R / Python ----
        with tabs[3]:
            s_title = st.text_input(t("resource_title_label"), key=f"st_{m['id']}")
            s_lang = st.selectbox(
                t("resource_sandbox_language_label"), ["python", "r"],
                format_func=lambda x: "Python" if x == "python" else "R",
                key=f"sl_{m['id']}",
            )
            s_code = st.text_area(
                t("resource_sandbox_starter_label"), height=180, key=f"sc_{m['id']}",
                value="print('Bonjour depuis le sandbox')" if st.session_state.get(f"sl_{m['id']}", "python") == "python"
                else "cat('Bonjour depuis le sandbox R')",
            )
            if st.button(t("admin_publish"), key=f"spub_{m['id']}", type="primary"):
                db.add_resource(m["id"], "sandbox", s_title.strip() or t("resource_sandbox"),
                                 language=s_lang, starter_code=s_code)
                st.success(t("admin_content_published"))
                st.rerun()

        # ---- Quiz ----
        with tabs[4]:
            q_title = st.text_input(t("resource_title_label"), key=f"qt_{m['id']}")
            n_q = st.number_input(t("resource_quiz_num_questions"), min_value=1, max_value=20, value=3, key=f"nq_{m['id']}")
            questions = []
            for qi in range(int(n_q)):
                st.markdown(f"**{t('resource_quiz_question')} {qi + 1}**")
                q_text = st.text_input(t("resource_quiz_question_label"), key=f"qq_{m['id']}_{qi}")
                opts_raw = st.text_area(
                    t("resource_quiz_options_label"), key=f"qo_{m['id']}_{qi}",
                    help=t("resource_quiz_options_help"),
                )
                opts = [o.strip() for o in opts_raw.split("\n") if o.strip()]
                correct = st.number_input(
                    t("resource_quiz_correct_label"), min_value=1,
                    max_value=max(len(opts), 1), value=1, key=f"qc_{m['id']}_{qi}",
                )
                questions.append({"question": q_text.strip(), "options": opts, "correct": int(correct) - 1})
            if st.button(t("admin_publish"), key=f"qpub_{m['id']}", type="primary"):
                valid = all(q["question"] and len(q["options"]) >= 2 for q in questions)
                if valid:
                    db.add_resource(m["id"], "quiz", q_title.strip() or t("resource_quiz"),
                                     quiz_json=json.dumps(questions, ensure_ascii=False))
                    st.success(t("admin_content_published"))
                    st.rerun()
                else:
                    st.warning(t("resource_quiz_missing"))

        # ---- Contenu déjà publié dans ce module ----
        resources = db.list_resources(m["id"])
        if resources:
            st.markdown(f"**{t('admin_existing_content')} ({len(resources)})**")
            for r in resources:
                rc1, rc2, rc3 = st.columns([5, 2, 1])
                with rc1:
                    st.markdown(f"{RESOURCE_ICONS.get(r['type'], '📄')} {r['title']}")
                with rc2:
                    st.caption(r["type"])
                with rc3:
                    if st.button("🗑️", key=f"delres_{r['id']}", use_container_width=True):
                        db.delete_resource(r["id"])
                        st.rerun()
