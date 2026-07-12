"""
i18n.py — Petit moteur de traduction FR / EN pour toute la plateforme.
Toutes les pages importent `t(key)` et lisent la langue depuis st.session_state["lang"].
"""
import streamlit as st

TRANSLATIONS = {
    # ---------- Navigation / global ----------
    "brand_tagline": {
        "fr": "Une statistique de qualité pour un développement harmonieux et une planification réussie",
        "en": "Quality statistics for harmonious development and successful planning",
    },
    "lang_button_label": {"fr": "🌐 English", "en": "🌐 Français"},
    "nav_home": {"fr": "Accueil", "en": "Home"},
    "nav_program": {"fr": "Programme", "en": "Program"},
    "nav_payment": {"fr": "Paiement & Inscription", "en": "Payment & Enrollment"},
    "nav_space": {"fr": "Mon espace", "en": "My learning space"},
    "nav_admin": {"fr": "Admin", "en": "Admin"},

    # ---------- Home ----------
    "special_training": {"fr": "FORMATION SPÉCIALE", "en": "SPECIAL TRAINING PROGRAM"},
    "training_title": {
        "fr": "Analyse des données de santé publique",
        "en": "Public Health Data Analysis",
    },
    "training_subtitle": {
        "fr": "Maîtrisez R, Python & Stata pour une prise de décision éclairée",
        "en": "Master R, Python & Stata for evidence-based decision making",
    },
    "organized_by": {
        "fr": "Organisée par **SCSM Group** et son label **Lab_Math**",
        "en": "Organized by **SCSM Group** and its **Lab_Math** label",
    },
    "cta_enroll": {"fr": "S'inscrire maintenant", "en": "Enroll now"},
    "cta_program": {"fr": "Voir le programme", "en": "View the program"},
    "logo_scsm_caption": {"fr": "Logo SCSM Group", "en": "SCSM Group logo"},
    "logo_labmath_caption": {"fr": "Logo Lab_Math", "en": "Lab_Math logo"},
    "logo_upload_hint": {
        "fr": "Aucun logo chargé pour le moment. L'administrateur peut l'ajouter depuis la page Admin.",
        "en": "No logo uploaded yet. The administrator can add it from the Admin page.",
    },
    "about_us_title": {"fr": "À propos de nous", "en": "About us"},
    "about_us_text": {
        "fr": (
            "SCSM Group — Statistic Consulting Survey & Multiservices — est un bureau d'étude "
            "érigé en structure accueillante, inclusive et novatrice, spécialisé dans la gestion "
            "des données statistiques et géospatiales, le montage de projets issus des problèmes "
            "de population ainsi que l'accompagnement technique des cabinets d'urbanisme et des ONG.\n\n"
            "À la pointe de la modernisation, nous proposons des formations certifiantes en Data "
            "Science (avec une dimension IA), en génie logiciel, en collecte et analyse avancée des "
            "données géospatiales, en Intelligence Artificielle et en Robotique.\n\n"
            "Notre label **Lab_Math** — laboratoire de Mathématiques appliquées et de modélisation "
            "des phénomènes démographiques — développe des solutions mathématiques innovantes pour "
            "relever les défis technologiques et industriels actuels."
        ),
        "en": (
            "SCSM Group — Statistic Consulting Survey & Multiservices — is a consulting firm built "
            "as a welcoming, inclusive and innovative structure, specialized in statistical and "
            "geospatial data management, in designing projects addressing population issues, and in "
            "the technical support of urban-planning firms and NGOs.\n\n"
            "At the forefront of modernization, we offer certified training in Data Science (with an "
            "AI dimension), software engineering, advanced geospatial data collection and analysis, "
            "Artificial Intelligence and Robotics.\n\n"
            "Our **Lab_Math** label — Applied Mathematics and Demographic Modeling Laboratory — "
            "develops innovative mathematical solutions to address today's technological and "
            "industrial challenges."
        ),
    },
    "objectives_title": {"fr": "Objectifs de la formation", "en": "Training objectives"},
    "objective_1": {
        "fr": "Acquérir les compétences clés en analyse de données de santé publique avec R, Python et Stata.",
        "en": "Acquire key skills in public health data analysis with R, Python and Stata.",
    },
    "objective_2": {
        "fr": "Maîtriser les techniques de collecte, nettoyage, visualisation et modélisation des données sanitaires.",
        "en": "Master collection, cleaning, visualization and modeling techniques for health data.",
    },
    "objective_3": {
        "fr": "Savoir interpréter et restituer les résultats pour éclairer les politiques et programmes de santé.",
        "en": "Learn to interpret and communicate results to inform health policies and programs.",
    },
    "objective_4": {
        "fr": "Utiliser les outils statistiques les plus répandus dans le secteur de la santé (épidémiologie, suivi-évaluation, enquêtes démographiques, etc.).",
        "en": "Use the most widely used statistical tools in the health sector (epidemiology, monitoring & evaluation, demographic surveys, etc.).",
    },
    "why_us_title": {"fr": "Pourquoi choisir SCSM Group & Lab_Math ?", "en": "Why choose SCSM Group & Lab_Math?"},
    "why_1": {"fr": "**Équipe pluridisciplinaire** — personnel compétent, talentueux et multitâches.", "en": "**Multidisciplinary team** — skilled, talented and versatile staff."},
    "why_2": {"fr": "**Outils modernes** — R, Python, Stata, Power BI, SPSS, SPAD, etc.", "en": "**Modern tools** — R, Python, Stata, Power BI, SPSS, SPAD, etc."},
    "why_3": {"fr": "**Approche pratique** — études de cas réels, exercices sur données sanitaires.", "en": "**Hands-on approach** — real case studies, exercises on health data."},
    "why_4": {"fr": "**Certification reconnue** — attestation délivrée par SCSM Group et Lab_Math.", "en": "**Recognized certification** — certificate issued by SCSM Group and Lab_Math."},
    "why_5": {"fr": "**Accompagnement personnalisé** — suivi post-formation et mise en réseau.", "en": "**Personalized support** — post-training follow-up and networking."},
    "locations_title": {"fr": "Lieux & dates", "en": "Locations & dates"},
    "locations_text": {
        "fr": "**Bertoua** (Siège social) · **Yaoundé** (Succursale) · **Bafoussam** (Succursale)\n\nDes représentants sont également présents dans d'autres localités.\n\nProchaines sessions : nous contacter pour les dates et modalités d'inscription.",
        "en": "**Bertoua** (Head office) · **Yaoundé** (Branch) · **Bafoussam** (Branch)\n\nRepresentatives are also present in other locations.\n\nUpcoming sessions: contact us for dates and registration details.",
    },
    "contact_title": {"fr": "Contact", "en": "Contact"},

    # ---------- Program page ----------
    "program_title": {"fr": "Programme — 3 modules complémentaires", "en": "Program — 3 complementary modules"},
    "target_audience_title": {"fr": "Public cible", "en": "Target audience"},
    "audience_1": {"fr": "Professionnels de la santé (médecins, épidémiologistes, pharmaciens, infirmiers)", "en": "Health professionals (doctors, epidemiologists, pharmacists, nurses)"},
    "audience_2": {"fr": "Chargés de suivi-évaluation et responsables de programmes de santé", "en": "Monitoring & evaluation officers and health program managers"},
    "audience_3": {"fr": "Chercheurs et enseignants-chercheurs en santé publique", "en": "Researchers and academics in public health"},
    "audience_4": {"fr": "Étudiants en master ou doctorat (santé publique, démographie, biostatistique)", "en": "Master's or PhD students (public health, demography, biostatistics)"},
    "audience_5": {"fr": "Consultants et bureaux d'études intervenant dans le domaine sanitaire", "en": "Consultants and consulting firms working in the health sector"},
    "module_col": {"fr": "Module", "en": "Module"},
    "content_col": {"fr": "Contenu", "en": "Content"},
    "software_col": {"fr": "Logiciel", "en": "Software"},
    "module_1_title": {"fr": "1 — Introduction & préparation", "en": "1 — Introduction & preparation"},
    "module_1_content": {"fr": "Collecte, nettoyage, gestion des bases de données sanitaires", "en": "Collection, cleaning, management of health databases"},
    "module_1_software": {"fr": "R, Python, Excel", "en": "R, Python, Excel"},
    "module_2_title": {"fr": "2 — Analyses statistiques & épidémiologiques", "en": "2 — Statistical & epidemiological analysis"},
    "module_2_content": {"fr": "Analyses descriptives, tests, régressions, analyses de survie", "en": "Descriptive analysis, tests, regressions, survival analysis"},
    "module_2_software": {"fr": "Stata, R, SPSS", "en": "Stata, R, SPSS"},
    "module_3_title": {"fr": "3 — Visualisation, modélisation avancée & IA", "en": "3 — Visualization, advanced modeling & AI"},
    "module_3_content": {"fr": "Tableaux de bord, modèles prédictifs, Machine Learning", "en": "Dashboards, predictive models, Machine Learning"},
    "module_3_software": {"fr": "Python (Pandas, Scikit-learn), R (Shiny, ggplot2), Power BI", "en": "Python (Pandas, Scikit-learn), R (Shiny, ggplot2), Power BI"},
    "services_title": {"fr": "Nos labels & services", "en": "Our labels & services"},
    "service_scsm": {"fr": "**SCSM Group** — Collecte et analyse de données, enquêtes, montage de projets, formation.", "en": "**SCSM Group** — Data collection and analysis, surveys, project design, training."},
    "service_labmath": {"fr": "**Lab_Math** — Modélisation mathématique, solutions innovantes, recherche appliquée.", "en": "**Lab_Math** — Mathematical modeling, innovative solutions, applied research."},
    "service_multi": {"fr": "**Multiservices** — bibliothèque à disposition, secrétariat technique avec infographes modernes.", "en": "**Multiservices** — library available, technical secretariat with modern graphic designers."},

    # ---------- Payment page ----------
    "payment_title": {"fr": "Paiement & Inscription", "en": "Payment & Enrollment"},
    "payment_intro": {
        "fr": "Choisissez le mode de paiement adapté à votre situation, puis déclarez votre paiement ci-dessous pour que l'administrateur puisse activer votre accès.",
        "en": "Choose the payment method that suits your situation, then declare your payment below so the administrator can activate your access.",
    },
    "local_payment_title": {"fr": "🇨🇲 Paiement local — Mobile Money", "en": "🇨🇲 Local payment — Mobile Money"},
    "momo_label": {"fr": "MTN Mobile Money (MoMo)", "en": "MTN Mobile Money (MoMo)"},
    "om_label": {"fr": "Orange Money (OM)", "en": "Orange Money (OM)"},
    "intl_payment_title": {"fr": "🌍 Paiement international — Carte bancaire", "en": "🌍 International payment — Bank card"},
    "intl_payment_text": {
        "fr": "Le paiement par carte bancaire (Visa/Mastercard) pour les participants internationaux sera bientôt disponible directement en ligne. En attendant, contactez l'administration pour recevoir un lien de paiement sécurisé.",
        "en": "Card payment (Visa/Mastercard) for international participants will soon be available directly online. In the meantime, contact the administration to receive a secure payment link.",
    },
    "bank_deposit_title": {"fr": "🏦 Dépôt bancaire", "en": "🏦 Bank deposit"},
    "bank_deposit_text": {
        "fr": "Pour un dépôt bancaire, veuillez contacter directement l'administration afin d'obtenir les coordonnées bancaires (RIB) et la procédure à suivre.",
        "en": "For a bank deposit, please contact the administration directly to obtain the bank details (IBAN/RIB) and the procedure to follow.",
    },
    "contact_admin_button": {"fr": "📞 Contacter l'administration", "en": "📞 Contact the administration"},
    "declare_payment_title": {"fr": "✅ Déclarer mon paiement", "en": "✅ Declare my payment"},
    "declare_payment_text": {
        "fr": "Une fois le paiement effectué, renseignez ce formulaire. Votre accès sera débloqué par un administrateur après vérification.",
        "en": "Once payment is made, fill in this form. Your access will be unlocked by an administrator after verification.",
    },
    "form_fullname": {"fr": "Nom complet", "en": "Full name"},
    "form_email": {"fr": "Adresse e-mail", "en": "Email address"},
    "form_phone": {"fr": "Téléphone", "en": "Phone number"},
    "form_method": {"fr": "Mode de paiement", "en": "Payment method"},
    "form_ref": {"fr": "Référence / N° de transaction", "en": "Reference / Transaction number"},
    "form_amount": {"fr": "Montant payé (FCFA ou devise)", "en": "Amount paid (FCFA or currency)"},
    "form_submit": {"fr": "Envoyer ma déclaration de paiement", "en": "Submit my payment declaration"},
    "form_success": {
        "fr": "Merci ! Votre déclaration a bien été enregistrée. Un administrateur va vérifier votre paiement et débloquer votre accès prochainement.",
        "en": "Thank you! Your declaration has been recorded. An administrator will verify your payment and unlock your access shortly.",
    },
    "form_missing": {"fr": "Merci de renseigner au minimum votre nom et votre e-mail.", "en": "Please fill in at least your name and email."},

    # ---------- Learning space page ----------
    "space_title": {"fr": "Mon espace d'apprentissage", "en": "My learning space"},
    "space_intro": {
        "fr": "Entrez l'adresse e-mail utilisée lors de votre inscription pour accéder à votre espace.",
        "en": "Enter the email address used during your registration to access your space.",
    },
    "space_email_input": {"fr": "Votre e-mail", "en": "Your email"},
    "space_check_button": {"fr": "Accéder à mon espace", "en": "Access my space"},
    "space_locked": {
        "fr": "🔒 Votre accès n'est pas encore activé. Si vous avez déjà payé, patientez pendant la vérification de l'administrateur, ou contactez-nous.",
        "en": "🔒 Your access is not yet activated. If you have already paid, please wait for administrator verification, or contact us.",
    },
    "space_not_found": {
        "fr": "Aucune déclaration de paiement trouvée pour cet e-mail. Rendez-vous sur la page Paiement & Inscription.",
        "en": "No payment declaration found for this email. Please go to the Payment & Enrollment page.",
    },
    "space_unlocked_title": {"fr": "🎉 Bienvenue dans votre espace !", "en": "🎉 Welcome to your space!"},
    "space_module_progress": {"fr": "Progression", "en": "Progress"},

    # ---------- Admin page ----------
    "admin_title": {"fr": "Espace administrateur", "en": "Administrator space"},
    "admin_password_label": {"fr": "Mot de passe administrateur", "en": "Administrator password"},
    "admin_login_button": {"fr": "Se connecter", "en": "Log in"},
    "admin_wrong_password": {"fr": "Mot de passe incorrect.", "en": "Incorrect password."},
    "admin_pending_title": {"fr": "Déclarations de paiement reçues", "en": "Received payment declarations"},
    "admin_unlock_title": {"fr": "🔓 Débloquer un espace d'apprentissage", "en": "🔓 Unlock a learning space"},
    "admin_unlock_text": {
        "fr": "Après avoir vérifié la réception du paiement, saisissez uniquement l'e-mail de l'apprenant ci-dessous pour débloquer son accès.",
        "en": "After verifying receipt of payment, enter only the learner's email below to unlock their access.",
    },
    "admin_unlock_email_input": {"fr": "E-mail de l'apprenant à débloquer", "en": "Learner's email to unlock"},
    "admin_unlock_button": {"fr": "Débloquer l'accès", "en": "Unlock access"},
    "admin_unlock_success": {"fr": "Accès débloqué pour", "en": "Access unlocked for"},
    "admin_lock_button": {"fr": "Reverrouiller", "en": "Re-lock"},
    "admin_no_pending": {"fr": "Aucune déclaration pour le moment.", "en": "No declarations yet."},
    "admin_logos_title": {"fr": "🖼️ Logos officiels", "en": "🖼️ Official logos"},
    "admin_upload_scsm": {"fr": "Charger le logo SCSM Group", "en": "Upload SCSM Group logo"},
    "admin_upload_labmath": {"fr": "Charger le logo Lab_Math", "en": "Upload Lab_Math logo"},
    "admin_logout": {"fr": "Se déconnecter", "en": "Log out"},
    "status_unlocked": {"fr": "Débloqué ✅", "en": "Unlocked ✅"},
    "status_pending": {"fr": "En attente ⏳", "en": "Pending ⏳"},

    # ---------- Modules & contenus pédagogiques (Admin) ----------
    "admin_modules_title": {"fr": "📚 Modules & contenus pédagogiques", "en": "📚 Modules & learning content"},
    "admin_modules_help": {
        "fr": "Ajoutez, réordonnez ou supprimez des modules, puis publiez pour chacun des vidéos, "
              "cours en texte, PDF, sandbox R/Python et quiz. Tout apparaît instantanément dans "
              "l'espace des candidats débloqués.",
        "en": "Add, reorder or delete modules, then publish videos, text lessons, PDFs, R/Python "
              "sandboxes and quizzes for each one. Everything appears instantly in unlocked "
              "candidates' learning space.",
    },
    "admin_add_module": {"fr": "➕ Ajouter un nouveau module", "en": "➕ Add a new module"},
    "module_title_fr": {"fr": "Titre du module (FR)", "en": "Module title (FR)"},
    "module_title_en": {"fr": "Titre du module (EN)", "en": "Module title (EN)"},
    "module_desc_fr": {"fr": "Description (FR)", "en": "Description (FR)"},
    "module_desc_en": {"fr": "Description (EN)", "en": "Description (EN)"},
    "admin_add_module_button": {"fr": "Créer le module", "en": "Create module"},
    "module_title_required": {"fr": "Le titre (FR) du module est obligatoire.", "en": "The module title (FR) is required."},
    "admin_module_added": {"fr": "✅ Module créé avec succès.", "en": "✅ Module created successfully."},
    "admin_no_modules": {
        "fr": "Aucun module pour le moment. Créez votre premier module ci-dessus.",
        "en": "No modules yet. Create your first module above.",
    },
    "admin_edit_module": {"fr": "✏️ Modifier ce module", "en": "✏️ Edit this module"},
    "admin_save_changes": {"fr": "Enregistrer les modifications", "en": "Save changes"},
    "admin_add_content": {"fr": "Publier du contenu dans ce module", "en": "Publish content in this module"},
    "resource_video": {"fr": "Vidéo", "en": "Video"},
    "resource_text": {"fr": "Cours en texte", "en": "Text lesson"},
    "resource_pdf": {"fr": "PDF", "en": "PDF"},
    "resource_sandbox": {"fr": "Sandbox R/Python", "en": "R/Python sandbox"},
    "resource_quiz": {"fr": "Quiz", "en": "Quiz"},
    "resource_title_label": {"fr": "Titre de la ressource", "en": "Resource title"},
    "resource_video_url_label": {"fr": "Lien vidéo externe (YouTube/Vimeo, optionnel)", "en": "External video link (YouTube/Vimeo, optional)"},
    "resource_video_file_label": {"fr": "Ou charger un fichier vidéo (mp4/webm/mov)", "en": "Or upload a video file (mp4/webm/mov)"},
    "resource_video_missing": {"fr": "Ajoutez un lien vidéo ou un fichier vidéo.", "en": "Add a video link or a video file."},
    "admin_publish": {"fr": "📤 Publier", "en": "📤 Publish"},
    "admin_content_published": {"fr": "✅ Contenu publié dans l'espace des candidats.", "en": "✅ Content published in the candidates' space."},
    "resource_text_content_label": {"fr": "Contenu du cours (Markdown accepté)", "en": "Lesson content (Markdown supported)"},
    "resource_text_missing": {"fr": "Le contenu du cours ne peut pas être vide.", "en": "Lesson content cannot be empty."},
    "resource_pdf_file_label": {"fr": "Charger un fichier PDF", "en": "Upload a PDF file"},
    "resource_pdf_missing": {"fr": "Veuillez charger un fichier PDF.", "en": "Please upload a PDF file."},
    "resource_sandbox_language_label": {"fr": "Langage", "en": "Language"},
    "resource_sandbox_starter_label": {"fr": "Code de départ (affiché au candidat)", "en": "Starter code (shown to the candidate)"},
    "resource_quiz_num_questions": {"fr": "Nombre de questions", "en": "Number of questions"},
    "resource_quiz_question": {"fr": "Question", "en": "Question"},
    "resource_quiz_question_label": {"fr": "Énoncé de la question", "en": "Question text"},
    "resource_quiz_options_label": {"fr": "Options de réponse (une par ligne)", "en": "Answer options (one per line)"},
    "resource_quiz_options_help": {"fr": "Saisissez chaque option de réponse sur une ligne séparée.", "en": "Enter each answer option on a separate line."},
    "resource_quiz_correct_label": {"fr": "N° de la bonne réponse", "en": "Correct answer number"},
    "resource_quiz_missing": {
        "fr": "Chaque question doit avoir un énoncé et au moins 2 options.",
        "en": "Each question needs text and at least 2 options.",
    },
    "admin_existing_content": {"fr": "Contenu déjà publié", "en": "Already published content"},

    # ---------- Modules & contenus pédagogiques (Espace candidat) ----------
    "space_no_modules": {
        "fr": "Aucun module n'a encore été publié par l'administrateur. Revenez bientôt !",
        "en": "No module has been published by the administrator yet. Check back soon!",
    },
    "resource_completed": {"fr": "Terminé", "en": "Completed"},
    "resource_video_unavailable": {"fr": "Vidéo non disponible.", "en": "Video not available."},
    "resource_mark_done": {"fr": "✅ Marquer comme terminé", "en": "✅ Mark as completed"},
    "resource_download_pdf": {"fr": "⬇️ Télécharger le PDF", "en": "⬇️ Download PDF"},
    "resource_pdf_unavailable": {"fr": "Fichier PDF non disponible.", "en": "PDF file not available."},
    "resource_sandbox_editor_label": {"fr": "Éditeur de code", "en": "Code editor"},
    "resource_sandbox_run": {"fr": "Exécuter le code", "en": "Run code"},
    "resource_sandbox_running": {"fr": "Exécution en cours…", "en": "Running…"},
    "resource_sandbox_success": {"fr": "✅ Code exécuté avec succès.", "en": "✅ Code ran successfully."},
    "resource_quiz_unavailable": {"fr": "Quiz non disponible.", "en": "Quiz not available."},
    "resource_quiz_pick_answer": {"fr": "Choisissez une réponse", "en": "Pick an answer"},
    "resource_quiz_submit": {"fr": "Valider mes réponses", "en": "Submit my answers"},
    "resource_quiz_result": {"fr": "Résultat", "en": "Result"},
    "resource_quiz_last_score": {"fr": "Dernier score enregistré", "en": "Last recorded score"},
}


def t(key: str) -> str:
    lang = st.session_state.get("lang", "fr")
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("fr", key))


def init_lang():
    if "lang" not in st.session_state:
        st.session_state["lang"] = "fr"


def toggle_lang():
    st.session_state["lang"] = "en" if st.session_state["lang"] == "fr" else "fr"
