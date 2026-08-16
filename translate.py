"""
translate.py — Traduction automatique instantanée (FR → EN) du contenu
pédagogique dynamique (cours, code de départ des sandbox, quiz) qui n'existe
qu'en une seule langue en base de données (contrairement aux modules et aux
textes d'interface, déjà bilingues).

Principe :
- On appelle un service de traduction gratuit (Google Translate, via la
  librairie `deep-translator`) uniquement quand la langue active est l'anglais.
- Chaque traduction est mise en cache de façon permanente dans la table SQLite
  `translation_cache` (voir db.py), indexée par un hash du texte source + la
  langue cible. Résultat : le tout premier apprenant à consulter un contenu en
  anglais déclenche un appel réseau (souvent < 1s), et TOUTES les consultations
  suivantes — par lui ou par n'importe quel autre apprenant — sont lues
  directement en base, donc réellement instantanées.
- Si le service de traduction est injoignable (pas de sortie réseau sur le VPS,
  service tiers en panne, quota dépassé…), on retombe silencieusement sur le
  texte original en français plutôt que de casser la page.
- Le code exécutable des sandbox n'est JAMAIS traduit : seuls les commentaires
  (lignes commençant par #, valable aussi bien en Python qu'en R) le sont, afin
  de ne jamais risquer de casser la syntaxe d'un exercice.
"""
import hashlib
import re

import db

try:
    from deep_translator import GoogleTranslator
    _TRANSLATOR_AVAILABLE = True
except ImportError:
    _TRANSLATOR_AVAILABLE = False

MAX_CHUNK_CHARS = 4000  # marge de sécurité sous la limite ~5000 car. de l'API


def _hash(text: str, target_lang: str, kind: str = "text") -> str:
    return hashlib.sha256(f"{kind}::{target_lang}::{text}".encode("utf-8")).hexdigest()


def _chunk(text: str, size: int = MAX_CHUNK_CHARS):
    """Découpe un texte long en morceaux traduisibles en un seul appel, en
    coupant de préférence entre paragraphes pour ne pas casser le sens."""
    if len(text) <= size:
        return [text]
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for p in paragraphs:
        candidate = f"{current}\n\n{p}" if current else p
        if len(candidate) > size and current:
            chunks.append(current)
            current = p
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks or [text]


def _call_translator(text: str, target_lang: str) -> str:
    return GoogleTranslator(source="auto", target=target_lang).translate(text)


def translate_text(text: str, target_lang: str = "en") -> str:
    """Traduit un texte libre (cours en Markdown, titre de ressource, question
    ou option de quiz…), avec mise en cache persistante. Retourne le texte
    d'origine si vide, si la langue cible est le français, ou en cas d'échec."""
    if not text or not text.strip() or target_lang == "fr" or not _TRANSLATOR_AVAILABLE:
        return text

    key = _hash(text, target_lang)
    cached = db.get_cached_translation(key)
    if cached is not None:
        return cached

    try:
        pieces = [_call_translator(chunk, target_lang) for chunk in _chunk(text)]
        translated = "\n\n".join(pieces)
    except Exception:
        return text

    db.set_cached_translation(key, target_lang, text, translated)
    return translated


_COMMENT_RE = re.compile(r"^(\s*#\s?)(.*)$")  # valable en Python ET en R


def translate_code_comments(code: str, target_lang: str = "en") -> str:
    """Traduit uniquement les commentaires d'un extrait de code R/Python (lignes
    commençant par #), en laissant le code exécutable strictement inchangé."""
    if not code or target_lang == "fr" or not _TRANSLATOR_AVAILABLE:
        return code

    key = _hash(code, target_lang, kind="code")
    cached = db.get_cached_translation(key)
    if cached is not None:
        return cached

    out_lines = []
    changed = False
    for line in code.split("\n"):
        m = _COMMENT_RE.match(line)
        comment = m.group(2).strip() if m else ""
        if m and comment:
            try:
                translated_comment = _call_translator(comment, target_lang)
                out_lines.append(f"{m.group(1)}{translated_comment}")
                changed = True
                continue
            except Exception:
                pass
        out_lines.append(line)

    result = "\n".join(out_lines)
    if changed:
        db.set_cached_translation(key, target_lang, code, result)
    return result
