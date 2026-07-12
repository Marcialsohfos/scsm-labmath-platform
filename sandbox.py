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

TIMEOUT_SECONDS = 8
MAX_OUTPUT_CHARS = 8000


def _truncate(text):
    if text and len(text) > MAX_OUTPUT_CHARS:
        return text[:MAX_OUTPUT_CHARS] + "\n… (sortie tronquée)"
    return text


def run_python(code: str):
    """Exécute du code Python dans un sous-processus isolé avec timeout."""
    with tempfile.TemporaryDirectory() as tmp:
        script_path = os.path.join(tmp, "candidate_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
        try:
            result = subprocess.run(
                ["python3", script_path],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            return {
                "ok": result.returncode == 0,
                "stdout": _truncate(result.stdout),
                "stderr": _truncate(result.stderr),
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "stdout": "", "stderr": f"⏱️ Temps d'exécution dépassé ({TIMEOUT_SECONDS}s)."}
        except Exception as e:
            return {"ok": False, "stdout": "", "stderr": str(e)}


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
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "stdout": "", "stderr": f"⏱️ Temps d'exécution dépassé ({TIMEOUT_SECONDS}s)."}
        except Exception as e:
            return {"ok": False, "stdout": "", "stderr": str(e)}


def run_code(language: str, code: str):
    if language == "python":
        return run_python(code)
    elif language == "r":
        return run_r(code)
    return {"ok": False, "stdout": "", "stderr": "Langage non supporté."}
