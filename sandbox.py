"""
sandbox.py — Exécution du code soumis par les apprenants dans les sandbox Python et R.

⚠️ Note de sécurité importante (à lire avant mise en production) :
Ce module exécute le code de l'apprenant dans un sous-processus séparé, avec un délai
maximal (timeout) et sans accès réseau garanti. C'est suffisant pour un usage interne,
avec un nombre limité d'apprenants de confiance (formation payante, accès débloqué
manuellement par l'admin). Ce n'est PAS un sandbox de niveau production capable
d'isoler complètement du code hostile : le sous-processus tourne sur la même machine
que l'application. Pour une exposition publique à grande échelle, il est recommandé de
déléguer l'exécution à un service dédié et isolé (conteneur éphémère par exécution,
ex. Docker/gVisor/Firecracker, ou une API tierce type Piston/Judge0) plutôt que de
lancer le code directement sur le serveur applicatif.
"""
import subprocess
import tempfile
import os
import shutil
import base64
import glob

TIMEOUT_SECONDS = 8
MAX_OUTPUT_CHARS = 8000
MAX_ARTIFACTS = 6
MAX_ARTIFACT_BYTES = 6_000_000  # 6 Mo par fichier

# Extensions qu'on cherche à récupérer dans le dossier de travail après exécution,
# et comment les afficher côté Streamlit.
_ARTIFACT_KINDS = {
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".svg": "image",
    ".html": "html", ".htm": "html",
    ".pdf": "pdf",
}


def _truncate(text):
    if text and len(text) > MAX_OUTPUT_CHARS:
        return text[:MAX_OUTPUT_CHARS] + "\n… (sortie tronquée)"
    return text


def _collect_artifacts(tmp, script_path):
    """Récupère les fichiers (images, cartes HTML, PDF) que le script a écrits dans
    son dossier de travail — ex: plt.savefig(), m.save(), ggsave(), saveWidget(),
    ou le Rplots.pdf que R génère automatiquement quand un plot() est appelé sans
    device explicite. C'est indispensable car aucun écran n'est disponible sur le
    serveur : rien ne s'affiche jamais tout seul, il faut le récupérer sous forme
    de fichier."""
    artifacts = []
    files = [
        p for p in sorted(glob.glob(os.path.join(tmp, "**", "*"), recursive=True), key=os.path.getmtime)
        if os.path.isfile(p) and p != script_path
    ]
    for path in files:
        ext = os.path.splitext(path)[1].lower()
        kind = _ARTIFACT_KINDS.get(ext)
        if not kind:
            continue
        try:
            size = os.path.getsize(path)
            if size == 0 or size > MAX_ARTIFACT_BYTES:
                continue
            if kind == "html":
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    data = f.read()
            else:
                with open(path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("ascii")
            artifacts.append({"type": kind, "filename": os.path.basename(path), "data": data})
        except OSError:
            continue
        if len(artifacts) >= MAX_ARTIFACTS:
            break
    return artifacts


def run_python(code: str):
    """Exécute du code Python dans un sous-processus isolé avec timeout."""
    with tempfile.TemporaryDirectory() as tmp:
        script_path = os.path.join(tmp, "candidate_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        env = os.environ.copy()
        # Pas d'écran sur le serveur : force matplotlib en mode "fichier uniquement"
        # pour éviter les erreurs silencieuses et permettre à plt.savefig() de fonctionner.
        env["MPLBACKEND"] = "Agg"
        try:
            result = subprocess.run(
                ["python3", script_path],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                env=env,
            )
            return {
                "ok": result.returncode == 0,
                "stdout": _truncate(result.stdout),
                "stderr": _truncate(result.stderr),
                "artifacts": _collect_artifacts(tmp, script_path),
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "stdout": "", "stderr": f"⏱️ Temps d'exécution dépassé ({TIMEOUT_SECONDS}s).", "artifacts": []}
        except Exception as e:
            return {"ok": False, "stdout": "", "stderr": str(e), "artifacts": []}


def r_available():
    return shutil.which("Rscript") is not None


def run_r(code: str):
    """Exécute du code R via Rscript si disponible sur le serveur, avec timeout."""
    if not r_available():
        return {
            "ok": False,
            "stdout": "",
            "stderr": (
                "R (Rscript) n'est pas installé sur ce serveur. Copiez le code et exécutez-le "
                "dans RStudio / R local, ou demandez à l'administrateur d'installer R sur le serveur."
            ),
        }
    with tempfile.TemporaryDirectory() as tmp:
        script_path = os.path.join(tmp, "candidate_script.R")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        try:
            result = subprocess.run(
                ["Rscript", "--vanilla", script_path],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            return {
                "ok": result.returncode == 0,
                "stdout": _truncate(result.stdout),
                "stderr": _truncate(result.stderr),
                "artifacts": _collect_artifacts(tmp, script_path),
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "stdout": "", "stderr": f"⏱️ Temps d'exécution dépassé ({TIMEOUT_SECONDS}s).", "artifacts": []}
        except Exception as e:
            return {"ok": False, "stdout": "", "stderr": str(e), "artifacts": []}


def run_code(language: str, code: str):
    if language == "python":
        return run_python(code)
    elif language == "r":
        return run_r(code)
    return {"ok": False, "stdout": "", "stderr": "Langage non supporté."}
