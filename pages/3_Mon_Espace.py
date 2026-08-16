import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components
from i18n import t, init_lang
from common import (
    apply_base_style, render_sidebar, module_title, module_description,
    module_dataset_dir, list_module_datasets,
)
import db
import sandbox
import translate

st.set_page_config(page_title="Mon espace — SCSM Group · Lab_Math", page_icon="🔐", layout="wide")
init_lang()
apply_base_style()
render_sidebar()
db.init_db()

# Langue active — sert à déclencher la traduction automatique (voir translate.py)
# de tout le contenu pédagogique qui n'existe qu'en français en base (cours,
# code de départ des sandbox, quiz). Les modules eux-mêmes restent bilingues
# "en dur" via title_fr/title_en (voir common.py).
lang = st.session_state.get("lang", "fr")

st.title(t("space_title"))
st.write(t("space_intro"))

email = st.text_input(t("space_email_input"), value=st.session_state.get("space_email", ""))
check = st.button(t("space_check_button"), type="primary")

if check and email:
    st.session_state["space_email"] = email.strip().lower()

active_email = st.session_state.get("space_email", "")

if active_email:
    reg = db.get_registration(active_email)
    if reg is None:
        st.warning(t("space_not_found"))
    elif not reg["unlocked"]:
        st.info(t("space_locked"))
    else:
        st.success(f"{t('space_unlocked_title')} — {reg['full_name'] or active_email}")
        st.write("")

        modules = db.list_modules()
        if not modules:
            st.info(t("space_no_modules"))

        for i, m in enumerate(modules):
            done, total = db.module_progress_ratio(active_email, m["id"])
            percent = int((done / total) * 100) if total else 0

            st.markdown('<div class="scsm-module-card scsm-card" style="margin-bottom:0.8rem;">', unsafe_allow_html=True)
            with st.expander(f"📦 {module_title(m)}  ·  {percent}%", expanded=(i == 0)):
                if module_description(m):
                    st.markdown(module_description(m))

                st.progress(percent / 100, text=f"{t('space_module_progress')} — {done}/{total}" if total else t("space_module_progress"))

                resources = db.list_resources(m["id"])
                if not resources:
                    st.caption(
                        "Les ressources (vidéos, PDF, sandbox R/Python, quiz) seront publiées ici par "
                        "l'administrateur au fur et à mesure de la formation."
                        if st.session_state["lang"] == "fr"
                        else "Resources (videos, PDFs, R/Python sandbox, quizzes) will be published "
                        "here by the administrator as the training progresses."
                    )

                for r in resources:
                    st.markdown('<div class="scsm-resource-row">', unsafe_allow_html=True)
                    completed = db.is_completed(active_email, r["id"])
                    r_title = translate.translate_text(r["title"] or "", lang)
                    st.markdown(f"#### 🎬 {r_title}" if r["type"] == "video" else
                                f"#### 📖 {r_title}" if r["type"] == "text" else
                                f"#### 📑 {r_title}" if r["type"] == "pdf" else
                                f"#### 💻 {r_title}" if r["type"] == "sandbox" else
                                f"#### ❓ {r_title}",
                                unsafe_allow_html=False)
                    if completed:
                        st.markdown(f"<span class='scsm-done-badge'>✓ {t('resource_completed')}</span>", unsafe_allow_html=True)

                    # ---------------- Vidéo ----------------
                    if r["type"] == "video":
                        if r["file_path"] and os.path.exists(r["file_path"]):
                            st.video(r["file_path"])
                        elif r["external_url"]:
                            st.video(r["external_url"])
                        else:
                            st.caption(t("resource_video_unavailable"))
                        if not completed:
                            if st.button(t("resource_mark_done"), key=f"donev_{r['id']}"):
                                db.mark_progress(active_email, r["id"])
                                st.rerun()

                    # ---------------- Cours en texte ----------------
                    elif r["type"] == "text":
                        st.markdown(translate.translate_text(r["text_content"] or "", lang))
                        if not completed:
                            if st.button(t("resource_mark_done"), key=f"donet_{r['id']}"):
                                db.mark_progress(active_email, r["id"])
                                st.rerun()

                    # ---------------- PDF ----------------
                    elif r["type"] == "pdf":
                        if r["file_path"] and os.path.exists(r["file_path"]):
                            with open(r["file_path"], "rb") as f:
                                st.download_button(
                                    t("resource_download_pdf"), data=f.read(),
                                    file_name=os.path.basename(r["file_path"]),
                                    mime="application/pdf", key=f"dlpdf_{r['id']}",
                                )
                        else:
                            st.caption(t("resource_pdf_unavailable"))
                        if not completed:
                            if st.button(t("resource_mark_done"), key=f"donep_{r['id']}"):
                                db.mark_progress(active_email, r["id"])
                                st.rerun()

                    # ---------------- Sandbox R / Python ----------------
                    elif r["type"] == "sandbox":
                        st.caption(f"{t('resource_sandbox_language_label')} : {'Python' if r['language']=='python' else 'R'}")

                        # Fichiers de données déposés par l'admin pour ce module (ex.
                        # patients_bertoua.xlsx) : copiés automatiquement dans le
                        # répertoire de travail du sandbox à chaque exécution, donc
                        # read_excel("patients_bertoua.xlsx") fonctionne tel quel.
                        module_datasets = list_module_datasets(m["id"])
                        if module_datasets:
                            st.caption(
                                (f"📂 Fichiers de données disponibles dans ce sandbox : "
                                 f"{', '.join(module_datasets)}")
                                if lang == "fr" else
                                (f"📂 Data files available in this sandbox: "
                                 f"{', '.join(module_datasets)}")
                            )

                        # Upload optionnel : fichiers propres à l'apprenant (en plus de
                        # ceux du module ci-dessus), utiles pour un exercice où chacun
                        # travaille sur son propre jeu de données. Conservés en mémoire
                        # de session le temps de la session (pas sur disque).
                        with st.expander(
                            "📎 Ajouter mes propres fichiers de données (optionnel)"
                            if lang == "fr" else
                            "📎 Add my own data files (optional)"
                        ):
                            own_files = st.file_uploader(
                                "Fichiers (.xlsx, .csv, .json, .txt)" if lang == "fr"
                                else "Files (.xlsx, .csv, .json, .txt)",
                                type=["xlsx", "xls", "csv", "json", "txt"],
                                accept_multiple_files=True,
                                key=f"upl_{r['id']}",
                            )
                            st.session_state[f"extra_files_{r['id']}"] = (
                                {f.name: f.getvalue() for f in own_files} if own_files else {}
                            )

                        # Seuls les commentaires du code de départ sont traduits (jamais le
                        # code exécutable). On ne réinitialise l'éditeur avec la version
                        # traduite QUE si l'apprenant n'a pas encore touché au code, pour ne
                        # jamais écraser un travail en cours en changeant de langue.
                        localized_starter = translate.translate_code_comments(r["starter_code"] or "", lang)
                        code_key = f"code_{r['id']}"
                        seed_key = f"{code_key}__seed"
                        seed_lang_key = f"{code_key}__seed_lang"
                        if code_key not in st.session_state:
                            st.session_state[code_key] = localized_starter
                            st.session_state[seed_key] = localized_starter
                            st.session_state[seed_lang_key] = lang
                        elif st.session_state.get(seed_lang_key) != lang:
                            if st.session_state[code_key] == st.session_state.get(seed_key):
                                st.session_state[code_key] = localized_starter
                                st.session_state[seed_key] = localized_starter
                            st.session_state[seed_lang_key] = lang

                        st.text_area(t("resource_sandbox_editor_label"), key=code_key, height=200)
                        run_col, done_col = st.columns([1, 1])
                        with run_col:
                            if st.button(f"▶️ {t('resource_sandbox_run')}", key=f"run_{r['id']}", type="primary"):
                                with st.spinner(t("resource_sandbox_running")):
                                    result = sandbox.run_code(
                                        r["language"], st.session_state[code_key],
                                        dataset_dir=module_dataset_dir(m["id"]),
                                        extra_files=st.session_state.get(f"extra_files_{r['id']}"),
                                    )
                                st.session_state[f"result_{r['id']}"] = result
                        with done_col:
                            if not completed:
                                if st.button(t("resource_mark_done"), key=f"dones_{r['id']}"):
                                    db.mark_progress(active_email, r["id"])
                                    st.rerun()
                        result = st.session_state.get(f"result_{r['id']}")
                        if result:
                            if result["stdout"]:
                                st.code(result["stdout"], language="text")

                            artifacts = result.get("artifacts", [])
                            for idx, art in enumerate(artifacts):
                                if art["type"] == "image":
                                    st.image(
                                        base64.b64decode(art["data"]),
                                        caption=art["filename"],
                                        use_container_width=True,
                                    )
                                elif art["type"] == "html":
                                    # Cartes leaflet/folium, widgets htmlwidgets, plotly, etc.
                                    components.html(art["data"], height=520, scrolling=True)
                                elif art["type"] == "pdf":
                                    st.download_button(
                                        f"📄 {art['filename']}",
                                        data=base64.b64decode(art["data"]),
                                        file_name=art["filename"],
                                        mime="application/pdf",
                                        key=f"dlart_{r['id']}_{idx}",
                                    )

                            if result["stderr"]:
                                st.error(result["stderr"])
                            if result["ok"] and not result["stderr"]:
                                st.success(t("resource_sandbox_success"))
                            if result["ok"] and not result["stdout"] and not artifacts:
                                st.info(t("resource_sandbox_no_output"))

                    # ---------------- Quiz ----------------
                    elif r["type"] == "quiz":
                        try:
                            questions = json.loads(r["quiz_json"] or "[]")
                        except (json.JSONDecodeError, TypeError):
                            questions = []
                        if not questions:
                            st.caption(t("resource_quiz_unavailable"))
                        else:
                            answers = {}
                            with st.form(f"quiz_form_{r['id']}"):
                                for qi, q in enumerate(questions):
                                    q_text = translate.translate_text(q["question"], lang)
                                    q_options = [translate.translate_text(opt, lang) for opt in q["options"]]
                                    st.markdown(f"**{qi + 1}. {q_text}**")
                                    answers[qi] = st.radio(
                                        t("resource_quiz_pick_answer"), options=list(range(len(q_options))),
                                        format_func=lambda idx, opts=q_options: opts[idx],
                                        key=f"quiz_{r['id']}_{qi}", label_visibility="collapsed",
                                    )
                                submitted = st.form_submit_button(t("resource_quiz_submit"), type="primary")
                            if submitted:
                                score = sum(1 for qi, q in enumerate(questions) if answers[qi] == q["correct"])
                                total_q = len(questions)
                                pct = int((score / total_q) * 100) if total_q else 0
                                db.mark_progress(active_email, r["id"], score=f"{score}/{total_q}")
                                if pct >= 50:
                                    st.success(f"{t('resource_quiz_result')} : {score}/{total_q} ({pct}%)")
                                    st.balloons()
                                else:
                                    st.warning(f"{t('resource_quiz_result')} : {score}/{total_q} ({pct}%)")
                                st.rerun()
                            prev_score = db.get_progress_score(active_email, r["id"])
                            if prev_score:
                                st.caption(f"{t('resource_quiz_last_score')} : {prev_score}")

                    st.markdown('</div>', unsafe_allow_html=True)
                    st.divider()
            st.markdown('</div>', unsafe_allow_html=True)
