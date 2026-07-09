# 📊 Plateforme SCSM Group · Lab_Math — Formation « Analyse des données de santé publique »

Plateforme web (Streamlit) pour la formation spéciale **Analyse des données de santé publique —
Maîtrisez R, Python & Stata**, organisée par **SCSM Group** et son label **Lab_Math**, inspirée
du niveau d'exigence de DataCamp / DataCamp for Government & Academic programs, et de
l'architecture déjà en place sur **Café_digit**.

## Comment ce projet se situe par rapport à Café_digit

Café_digit (votre plateforme existante) utilise React + Node/Express + PostgreSQL/Prisma — une
architecture robuste, multi-utilisateurs, avec sandbox R (webR) et back-office complet.

Pour **cette nouvelle plateforme**, la contrainte imposée est différente : l'interface **publique
(cliente)** doit être réalisée avec **Streamlit** (streamlit.io). Streamlit ne permettant pas
nativement une architecture multi-tables/API séparée façon Café_digit, ce projet reprend les
**mêmes concepts** (déclaration de paiement → validation admin → déblocage de l'accès) mais avec
une pile technique 100 % Python, plus rapide à déployer pour une formation ponctuelle :

| | Café_digit | Cette plateforme (SCSM/Lab_Math) |
|---|---|---|
| Frontend public | React + Vite + Tailwind | **Streamlit** (imposé) |
| Backend | Node/Express + Prisma | Logique intégrée dans les pages Streamlit |
| Base de données | PostgreSQL | **SQLite** (fichier `data/platform.db`, suffisant pour une formation, migrable vers PostgreSQL si le volume d'apprenants augmente) |
| Auth apprenant | JWT (email + mot de passe) | Accès par **e-mail** débloqué manuellement par l'admin (comme demandé) |
| Paiement | Mobile money, validation manuelle admin | **MoMo, Orange Money, carte bancaire (à venir), dépôt bancaire** + déclaration + validation manuelle admin |
| Déploiement | Docker (3 conteneurs) | Un seul processus Streamlit (+ Docker fourni) |

## Fonctionnalités livrées (conformes à votre cahier des charges)

- ✅ Interface **responsive**, style moderne façon DataCamp (hero, cartes, sections)
- ✅ Contenu de la **FORMATION SPÉCIALE** intégralement repris du flyer (objectifs, 3 modules,
  public cible, pourquoi nous choisir, lieux/dates, contacts)
- ✅ Bouton **🌐 FR ⇄ EN** dans la barre latérale, actif sur **toutes les pages**
- ✅ **Emplacements réservés** pour les logos réels de SCSM Group et Lab_Math (visibles sur toutes
  les pages), **modifiables par l'admin** via upload — aucun code à toucher
- ✅ Interface **publique en Streamlit** (comme demandé, façon streamlit.io)
- ✅ Page **Paiement & Inscription** :
  - Numéros **MTN MoMo** et **Orange Money** pour les paiements locaux
  - Espace **carte bancaire** pour les internationaux
  - Bouton **Contacter l'administration** pour un dépôt bancaire
  - Formulaire de **déclaration de paiement** (nom, e-mail, téléphone, mode, référence, montant)
- ✅ Page **Mon espace** : l'apprenant entre son e-mail ; s'il est débloqué, il voit le contenu des
  3 modules (progression, ressources à publier par l'admin)
- ✅ Page **Admin** protégée par mot de passe :
  - Liste de toutes les déclarations de paiement reçues
  - Champ dédié où l'admin saisit **uniquement l'e-mail** de l'apprenant pour **débloquer** son
    espace (fonctionnalité demandée explicitement)
  - Gestion des logos (upload)

## Structure du projet

```
scsm-labmath-platform/
├── app.py                          # Page d'accueil (Streamlit entry point)
├── common.py                       # Sidebar, style, emplacements logo partagés
├── db.py                           # Persistance SQLite (déclarations, réglages/logos)
├── i18n.py                         # Dictionnaire de traduction FR/EN + bouton toggle
├── pages/
│   ├── 1_Programme.py              # Programme détaillé (3 modules, public cible, services)
│   ├── 2_Paiement_Inscription.py   # MoMo / OM / carte bancaire / dépôt bancaire + formulaire
│   ├── 3_Mon_Espace.py             # Espace apprenant (accès par e-mail débloqué)
│   └── 4_Admin.py                  # Back-office : déblocage par e-mail, logos, suivi paiements
├── assets/                         # Logos réels uploadés par l'admin (vide au départ)
├── data/                           # Base SQLite (créée automatiquement)
├── .streamlit/
│   ├── config.toml                 # Thème (couleurs SCSM)
│   └── secrets.toml.example        # Modèle pour le mot de passe admin
└── requirements.txt
```

## Démarrage rapide

```bash
cd scsm-labmath-platform
pip install -r requirements.txt

# Définir le mot de passe administrateur (recommandé) :
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# puis éditez .streamlit/secrets.toml et changez ADMIN_PASSWORD

streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`.

Mot de passe admin par défaut (si non configuré) : `changeme123` — **à changer avant toute mise
en ligne publique**.

## Déploiement en ligne

Options simples et gratuites/peu coûteuses, cohérentes avec l'esprit « streamlit.io » demandé :

1. **Streamlit Community Cloud** (share.streamlit.io) — connectez ce dépôt GitHub, définissez
   `ADMIN_PASSWORD` dans les "Secrets" de l'app. Gratuit pour un usage de formation.
2. **Serveur propre / VPS** avec Docker (un `Dockerfile` minimal peut être ajouté sur demande) et
   un reverse proxy (Caddy/Nginx) pour le TLS et le nom de domaine (ex. `formation.scsmaubmar.org`).

## Prochaines étapes suggérées

1. **Logos réels** : connectez-vous à `/pages/4_Admin.py` avec le mot de passe admin et uploadez
   les fichiers PNG/SVG officiels de SCSM Group et Lab_Math — ils s'afficheront automatiquement
   partout.
2. **Passerelle de paiement automatique** : remplacer la déclaration manuelle par une vraie API
   MTN MoMo / Orange Money (comme évoqué pour Café_digit), pour un déblocage automatique sans
   intervention admin.
3. **Carte bancaire internationale** : intégrer Stripe ou PayPal pour un paiement en ligne réel
   (actuellement : message d'attente + contact admin).
4. **Notifications e-mail** automatiques à l'apprenant lors du déblocage de son accès.
5. **Contenu pédagogique** : ajouter vidéos, PDF et sandbox R/Python directement dans
   `pages/3_Mon_Espace.py` module par module au fil de la formation.
6. **Passage à PostgreSQL** si le nombre d'apprenants dépasse quelques centaines (le code SQLite
   actuel migre facilement grâce à une couche `db.py` isolée).
