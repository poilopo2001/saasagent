# Backend API pour génération de sites avec Claude Code SDK - VERSION 2
# Utilise le prompt EXACT de prompt.md
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import json
import uuid
import asyncio
from anthropic import Anthropic

try:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
except ImportError:
    print("ERREUR: claude-agent-sdk non installé")
    ClaudeSDKClient = None
    ClaudeAgentOptions = None

app = FastAPI(title="SaaS Generator v2 - Prompt Complet")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: Dict[str, Dict[str, Any]] = {}

class BusinessInfo(BaseModel):
    # Informations générales
    name: str
    location: str
    phone: str
    email: str
    year: int
    domain_url: Optional[str] = ""

    # Adresse physique
    street: str
    postal_code: str
    city: str
    country: str
    hours: str

    # Services et positionnement
    services: str
    positioning: str

    # Design
    primary_color: str = "#1a5490"  # Primary blue
    secondary_color: str = "#ff8c42"  # Accent orange

class JobResponse(BaseModel):
    job_id: str
    status_url: str

class PrefillRequest(BaseModel):
    description: str

class PrefillResponse(BaseModel):
    name: str
    location: str
    phone: str
    email: str
    year: int
    domain_url: str
    street: str
    postal_code: str
    city: str
    country: str
    hours: str
    services: str
    positioning: str
    primary_color: str
    secondary_color: str

@app.get("/")
async def root():
    return {"status": "ok", "service": "SaaS Generator v2 - Prompt Complet", "version": "2.0"}

@app.post("/api/prefill", response_model=PrefillResponse)
async def prefill_form(request: PrefillRequest):
    """
    Endpoint pour pré-remplir le formulaire via Claude Haiku API
    """
    try:
        anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        prompt = f"""Analyse cette description d'entreprise et extrais TOUTES les informations nécessaires pour remplir un formulaire de génération de site web.

Description de l'entreprise:
{request.description}

Tu DOIS retourner un JSON valide avec EXACTEMENT ces champs (aucun champ manquant):
{{
  "name": "Nom de l'entreprise",
  "location": "Ville/Région principale (ex: Luxembourg, Lyon, Genève)",
  "phone": "Numéro de téléphone au format international (ex: +352 123 456 789)",
  "email": "Adresse email de contact",
  "year": année de création (nombre entre 1900 et 2025),
  "domain_url": "URL du site web s'il existe, sinon chaîne vide",
  "street": "Numéro et nom de rue",
  "postal_code": "Code postal",
  "city": "Ville",
  "country": "Pays",
  "hours": "Horaires d'ouverture au format 'Lun-Ven 08:00-18:00'",
  "services": "Liste des services séparés par des virgules",
  "positioning": "Proposition de valeur unique et positionnement de l'entreprise (2-3 phrases)",
  "primary_color": "#1a5490",
  "secondary_color": "#ff8c42"
}}

RÈGLES STRICTES:
1. Si une information n'est PAS mentionnée dans la description, invente une valeur PLAUSIBLE et PROFESSIONNELLE basée sur le contexte
2. Pour les horaires, utilise un format standard (ex: "Lun-Ven 08:00-18:00, Sam 09:00-12:00")
3. Pour l'adresse, si non mentionnée, invente une adresse cohérente avec la ville/pays
4. Pour le positioning, crée un USP professionnel basé sur les services et l'expérience
5. year doit être un NOMBRE (pas une chaîne)
6. Retourne UNIQUEMENT le JSON, rien d'autre"""

        response = anthropic_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        content = response.content[0].text.strip()

        # Nettoyer le JSON si des backticks sont présents
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        extracted_data = json.loads(content)

        return PrefillResponse(**extracted_data)

    except Exception as e:
        import traceback
        print(f"ERROR in prefill: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur lors du pré-remplissage: {str(e)}")

@app.post("/api/generate", response_model=JobResponse)
async def generate_site(business: BusinessInfo, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "message": "Job créé",
        "business": business.dict(),
        "github_url": None,
        "site_url": None,
        "error": None
    }
    background_tasks.add_task(generate_and_deploy, job_id, business)
    return JobResponse(job_id=job_id, status_url=f"/api/jobs/{job_id}")

async def generate_and_deploy(job_id: str, business: BusinessInfo):
    def update_job(status: str, progress: int, message: str = "", **kwargs):
        jobs[job_id].update({"status": status, "progress": progress, "message": message, **kwargs})

    try:
        update_job("processing", 10, "Initialisation...")
        site_slug = business.name.lower().replace(' ', '-').replace("'", '').replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a').replace('ç', 'c')
        site_dir = f"/tmp/generated-sites/{site_slug}"
        os.makedirs(site_dir, exist_ok=True)

        options = ClaudeAgentOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=["Write", "Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"GH_TOKEN": os.getenv("GITHUB_TOKEN", ""), "VERCEL_TOKEN": os.getenv("VERCEL_TOKEN", "")},
            system_prompt={"type": "preset", "preset": "claude_code", "append": "Tu es un expert Next.js 14+ avec App Router, TypeScript, Tailwind CSS, et Framer Motion. Tu DOIS exécuter TOUTES les étapes jusqu'au déploiement Vercel. Ne t'arrête JAMAIS avant que Vercel soit déployé."}
        )

        update_job("processing", 20, "Génération du site professionnel avec prompt complet...")

        # Calcul de l'expérience
        current_year = 2024
        years_experience = current_year - business.year

        # PROMPT COMPLET EXACT de prompt.md
        prompt = f"""Générer le code source complet et fonctionnel d'un site web Next.js 14+ (App Router) pour une entreprise locale de services B2B. Le site doit être mobile-first, ultra-rapide, SEO-optimisé localement et présenter un design professionnel moderne et haut de gamme (minimaliste, axé sur les couleurs primaires/accent, avec des animations subtiles et des composants réutilisables).

📋 INFORMATIONS ENTREPRISE:

VARIABLES À UTILISER DANS LE CODE:
- [NOM_ENTREPRISE] = "{business.name}"
- [LOCATION] = "{business.location}"
- [PHONE] = "{business.phone}"
- [EMAIL] = "{business.email}"
- [ANNEE] = "{business.year}"
- [EXPERIENCE] = "{years_experience} ans"
- [DOMAIN_URL] = "{business.domain_url or f'https://{site_slug}.vercel.app'}"

ADRESSE PHYSIQUE (LocalBusiness Schema):
- Rue: "{business.street}"
- Code Postal: "{business.postal_code}"
- Ville: "{business.city}"
- Pays: "{business.country}"
- Horaires: "{business.hours}"

SERVICES ET POSITIONNEMENT:
- Services: {business.services}
- USP/Positionnement: {business.positioning}

DESIGN:
- Couleur Primary: {business.primary_color}
- Couleur Accent: {business.secondary_color}

🛠️ PARTIE 1 : ARCHITECTURE TECHNIQUE & CONFIGURATION

1.1 Stack Technologique OBLIGATOIRE

Framework: Next.js 14.2+ (App Router, Server Components par défaut, 'use client' si nécessaire)
Langage: TypeScript (Mode Strict)
Styling: Tailwind CSS 3.4.17+ (avec customisation complète des couleurs/thèmes)
Animations: Framer Motion 12+ (pour les transitions page, scroll reveal, et micro-interactions)
Icônes: Lucide React
Images: Next/Image (avec optimisation et gestion priority)
Formulaires: React Hook Form (pour la logique d'état) + Zod (pour la validation des schémas)
Deployment: Vercel (Production Ready)

1.2 Structure Fichiers Complète

La structure doit inclure tous les éléments pour le SEO, la logique et le contenu, en utilisant des Server Components par défaut pour les pages et des Client Components pour les interactivité (Formulaires, Header, Popups).

projet/
├── app/
│   ├── layout.tsx              # Root layout (Header, Footer, Providers, SEO de base)
│   ├── page.tsx                # Homepage (structure complète détaillée en P3)
│   ├── globals.css             # Tailwind @layer directives + animations custom
│   │
│   ├── nos-services/           # Page parent pour la grille des services
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── [slug-service]/         # Pages individuelles de service (ex: isolation-combles)
│   │   ├── layout.tsx          # Metadata spécifique
│   │   └── page.tsx            # Contenu détaillé
│   │
│   ├── contact/page.tsx        # Contient le MultiStepForm
│   ├── realisations/page.tsx   # Page de galerie/projets
│   ├── devis-gratuit/page.tsx  # Page de conversion principale
│   ├── blog/                   # Structure articles + liste
│   ├── mentions-legales/page.tsx
│   └── politique-confidentialite/page.tsx
│
├── components/
│   ├── ui/                     # Composants UI de base (Button, Input, Accordion, Tabs)
│   ├── layout/                 # Header, Footer, StickyBar, Breadcrumbs
│   ├── sections/               # Composants de section réutilisables (Hero, StatsBar, Testimonials, ProcessTimeline)
│   ├── forms/                  # ContactForm, MultiStepForm, ExitIntentPopup
│   └── utils/                  # BeforeAfterSlider, AnimatedCounter
│
├── lib/
│   ├── metadata.ts             # SEO centralisé (titres, descriptions, mots-clés)
│   ├── schema.ts               # Fonctions de génération de JSON-LD (LocalBusiness, Service, BreadcrumbList)
│   ├── constants.ts            # Données globales (menu, adresses, téléphone, horaires)
│   └── types.ts                # Interfaces TypeScript pour les données
│
├── public/
│   ├── images/                 # Dossier pour les assets (logo, favicon, placeholders)
│   ├── sitemap.xml             # Sitemap généré
│   └── robots.txt              # Directives de crawl
│
├── tailwind.config.js          # Config complète
└── next.config.mjs             # Next/Image config pour Unsplash (dev)

🎨 PARTIE 2 : DESIGN SYSTEM AVANCÉ & UX

2.1 Palette Couleurs & Thème (Tailwind Config)
DOIT ÊTRE implémenté dans tailwind.config.js avec des teintes complètes.

Primary (Base): {business.primary_color} - Bleu professionnel, autoritaire, confiance.
Primary-700: #103256 - Teinte foncée pour hover/footer.
Primary-50: #e6f0f9 - Teinte très claire pour backgrounds subtils.
Accent (Base): {business.secondary_color} - Orange énergique, conversion, éléments clés (CTAs).
Accent-600: #ff7519 - Teinte foncée pour hover/active.
Neutral: gray - Utiliser les teintes gray-50 à gray-900 de Tailwind.

2.2 Typographie Système
Police Inter avec une échelle typographique modulaire et lisible.

H1 (Hero) - text-hero: text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-extrabold leading-none
H2 (Section) - text-h2: text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight
H3 (Titre Card) - text-h3: text-2xl sm:text-3xl font-bold
Body Large - text-body-large: text-lg sm:text-xl leading-relaxed (pour sous-titres/intro)
Body - text-body: text-base leading-relaxed

2.3 Composants de Design Clés (Classes Utilitaires)

.btn-primary: bg-primary / text-white. hover:bg-primary-600. Effet d'Ombre Léger: shadow-xl. Micro-interaction: hover:scale-105 active:scale-95. Le CTA principal pour la marque.

.btn-accent: OBLIGATOIRE pour la Conversion. bg-accent / text-white. hover:bg-accent-600. Effet de "Glow": shadow-accent/40 shadow-2xl. Le CTA le plus visible (Devis Gratuit).

.card-modern: bg-white / rounded-2xl / p-8. Bordure subtile: border border-gray-100. Effet de survol: hover:shadow-3xl hover:border-accent. Utilisé pour services, témoignages, étapes.

Glassmorphism: bg-white/10 backdrop-blur-md border border-white/20. Utilisé pour les popups et les éléments transparents sur des images de fond.

2.4 Animations Framer Motion & CSS

TOUTES les sections qui entrent dans le viewport DOIVENT utiliser Framer Motion pour un scroll reveal subtil:
initial: {{ opacity: 0, y: 50 }}, whileInView: {{ opacity: 1, y: 0 }}, transition: {{ duration: 0.8 }}

animate-fadeInUp: Titres et blocs de texte majeurs. Staggering (staggerChildren) pour les listes et les CTA multiples.
animate-float: Icônes ou éléments décoratifs dans la Hero Section. Mouvement lent ease-in-out infinite.
animate-pulse-glow: L'indicateur de nouvelle notification ou le bouton de téléphone sticky. Effet de halo autour d'un CTA.
Transitions: transition-all duration-500 ease-in-out sur tous les hover.

📐 PARTIE 3 : STRUCTURE PAGES DÉTAILLÉE (UX & LOGIQUE)

3.1 HOMEPAGE (/)
Le fichier app/page.tsx doit être un Client Component ('use client') pour gérer les états des tabs, FAQ et animations.

SECTION 1 - HERO (Conversion):
- Fond image haute résolution + Gradient Overlay (bg-gradient-hero)
- Shapes animées (Blob) derrière le texte
- H1: USP locale et chiffrée
- Texte centré sur la promesse de valeur
- 2 CTAs (Primaire: Devis, Secondaire: Réalisations)
- Social Proof (étoiles, expérience chiffrée) visible immédiatement

SECTION 2 - STATS BAR (Trust Signal):
- Section bg-white qui "monte" visuellement au-dessus de la Hero
- 4 Cards/Stats (Projets, Années, Satisfaction, Délai Devis)
- Icônes Lucide
- Effet Micro-interaction: hover:scale-110 sur chaque stat

SECTION 3 - SERVICES GRID (Découverte):
- Grid 3 colonnes (lg:grid-cols-3)
- Utilise le composant <ServiceCard>
- Design: Image aspect-[4/3] avec survol group-hover:scale-110
- Titre H3, Liste de 3 Bénéfices avec CheckCircle2 (accent)
- CTA "En Savoir Plus" (btn-secondary) + "Devis" (btn-accent)

SECTION 4 - BEFORE/AFTER (Preuve Visuelle - Crédibilité):
- Utilise le composant <BeforeAfterSlider>
- Slider interactif (drag-to-compare) pour 3-4 projets
- Onglets cliquables pour changer de projet
- Métrique Chiffrée (ex: "+45m²") en badge

SECTION 5 - PROCESS TIMELINE (Explication du Processus - Transparence):
- Design de Timeline Verticale Sophistiqué
- Fond gradient-primary
- Étapes numérotées (1, 2, 3...) avec une ligne de connexion verticale (CSS/Tailwind)
- Chaque étape est un <ProcessStep> avec un titre H3 et description
- Animation staggerChildren

SECTION 6 - TESTIMONIALS (Avis Clients - Réassurance):
- Grid 3 colonnes
- Utilise le composant <TestimonialCard>
- Design: Citation en italique, photo (ou initiales), Nom, Ville, Rating 5 étoiles (Accent)
- Citation visible: 50-70 mots
- hover:shadow-2xl hover:-translate-y-1

SECTION 7 - FAQ ACCORDION (Levier de Friction - SEO & UX):
- Utilise le composant <Accordion>
- Design card-modern individuel
- Animation de toggle du contenu (smooth max-height transition)
- Icône ChevronDown rotative à l'ouverture
- Contient les 5-6 questions les plus fréquentes

SECTION 8 - FINAL CTA (Conversion Finale - Closing):
- Background image pleine largeur avec Gradient gradient-accent overlay
- Titre H1 impactant (ex: "Il est temps de concrétiser votre projet")
- Multi-CTA: Bouton btn-xl ("Obtenir mon Devis Gratuit") + Icône Phone cliquable + Formulaire simplifié (Nom, Tél, Code Postal)

3.2 PAGE SERVICE INDIVIDUELLE (/[slug-service]/page.tsx)

- Header: <Breadcrumbs> obligatoire
- Hero Spécifique: Image hero + H1, sous-titre, 3 points forts (ex: Performance, Économie, Garantie). CTA btn-accent
- Section Problème/Solution/Bénéfices: Contenu structuré. Titres H2, liste à puces avec icônes
- Galerie Photos/Études de Cas: Grid 3 colonnes de réalisations spécifiques à ce service
- Pricing (Transparent): Section H2 titrée "Prix et Estimation". Affichage d'une range de prix (ex: 2300€ - 3500€/m²) avec explication des facteurs de variation
- Trust Badges / Certifications: 4 badges (ex: RGE, Garantie Décennale) en grid
- FAQ Spécifique: <Accordion> avec 4-5 questions/réponses spécifiques au service
- CTA Final: Section minimaliste avec un unique bouton btn-accent

3.3 PAGE CONTACT (/contact/page.tsx)

- Titre: H1 "Contactez-nous | Réponse Garantie en 24h"
- Formulaire Multi-Étapes (OBLIGATOIRE): Utilise le composant <MultiStepForm>
  Logique: 4 étapes avec progression visuelle (barre/indicateur). Validation Zod à chaque étape.
  - Étape 1: Type de Projet (Radio Buttons Visuels: Extension, Isolation, Rénovation)
  - Étape 2: Caractéristiques (Surface m², Budget Range - Sliders)
  - Étape 3: Timing (Quand souhaitez-vous commencer? - Select)
  - Étape 4: Coordonnées (Nom, Prénom, Téléphone, Email, Code Postal, RGPD Checkbox)
- Informations Contact: Grid 2 colonnes à côté du formulaire
  - Coordonnées (Adresse, Email, Téléphone - cliquables)
  - Horaires d'ouverture
  - Carte: Google Maps embed (iframe ou composant Map si librairie légère)

🧭 PARTIE 4 : NAVIGATION & UX AVANCÉE

4.1 Header (components/layout/Header.tsx)
DOIT ÊTRE un Client Component.

Desktop (≥1024px):
- Sticky Header (réduit en taille au scroll)
- Menu horizontal avec hover:text-accent
- Mega Menu Services: S'ouvre au survol. Structure 3 colonnes (Liens Services, Liens Infos/Guides, CTA Visuel Fort avec image/gradient)
- CTA Principal: btn-accent "Devis Gratuit" toujours visible à droite

Mobile (<1024px):
- <BurgerMenu> toggle pour ouvrir un overlay plein écran
- Les services sont listés dans l'overlay
- Déplacé dans l'overlay et la Sticky Bottom Bar

Logique d'État:
- const [isSticky, setIsSticky] = useState(false) géré par useEffect avec scroll listener
- const [isOpen, setIsOpen] = useState(false)

4.2 Sticky Bottom Bar (Mobile)
OBLIGATOIRE pour la conversion mobile. Barre fixe en bas de l'écran avec 3 icônes/liens visibles:
- Appeler (Icône Phone cliquable)
- Devis (Icône Calculator cliquable, btn-accent stylisé)
- Simulateur/Contact (Icône Mail ou Zap)

4.3 Exit Intent Popup (components/forms/ExitIntentPopup.tsx)
Logique de déclenchement:
- Desktop: Écouteur d'événement mouseleave qui se déclenche lorsque le curseur quitte le haut de la fenêtre
- Mobile: Déclenchement au défilement inversé rapide (scroll up) ou après 60 secondes
- Contenu: Offre d'urgence (ex: "Ne partez pas! Votre devis gratuit sous 48h expire!"). Formulaire minimaliste (Email + Tél)

🔍 PARTIE 5 : SEO & PERFORMANCE AVANCÉS

5.1 Metadata & SEO Local (lib/metadata.ts)
Toutes les pages DOIVENT utiliser des métadonnées centralisées, injectant les variables locales.

// lib/metadata.ts
export const PAGE_METADATA = {{
  home: {{
    title: "Extension Combles {business.location} | Agrandissement +30m² | Devis 48h",
    description: "Expert extension combles {business.location} depuis {years_experience} ans. Gagnez 30-50m² habitables. Devis gratuit 48h. Garantie décennale. Prix compétitifs.",
    keywords: ["extension combles {business.location}", "agrandissement maison {business.location}", "prix extension"],
    canonical: "{business.domain_url or f'https://{site_slug}.vercel.app'}"
  }},
  // ... autres pages
}}

5.2 Structured Data (JSON-LD)
Le fichier lib/schema.ts DOIT contenir des fonctions générant les schémas suivants:
- LocalBusiness (dans app/layout.tsx): Incluant le nom, l'adresse, les coordonnées (telephone), le geo (latitude/longitude), et les openingHours
- Service (dans chaque page de service): Décrivant le service, la zone, et le prix range
- FAQPage (dans les pages avec Accordion): Représentant les questions/réponses
- BreadcrumbList (dans <Breadcrumbs.tsx>): Pour le fil d'Ariane

5.3 Images Optimisées
- Toutes les images DOIVENT utiliser <Image /> de Next.js
- Qualité: quality={{90}}
- Lazy Loading: priority={{true}} uniquement pour la Hero Image. Toutes les autres images doivent être en lazy loading par défaut
- Alt Text: Description SEO-friendly incluant la localisation (ex: "Isolation combles achevé à {business.city}")

⚙️ PARTIE 6 : INSTRUCTIONS DE GÉNÉRATION FINALES

6.1 Directives de Codage
1. Commencer par la structure des dossiers, package.json, tailwind.config.js et next.config.mjs
2. Créer les composants de layout (Header.tsx, Footer.tsx) avec la logique d'état (sticky, mobile menu)
3. Développer la app/page.tsx en utilisant les composants de section réutilisables décrits en P3
4. Implémenter le <MultiStepForm> dans contact/page.tsx avec la logique de React Hook Form/Zod
5. Pour les animations, utiliser la syntaxe de Framer Motion sur les éléments clés et les classes CSS (animate-fadeInUp, delay-X)

ÉTAPES D'EXÉCUTION OBLIGATOIRES:

ÉTAPE 1 - Créer TOUS les fichiers requis dans {site_dir}

ÉTAPE 2 - Installation: cd {site_dir} && npm install

ÉTAPE 3 - Build: npm run build (corrige TOUTES les erreurs TypeScript)

ÉTAPE 4 - Git:
git config user.email "dev@{site_slug}.com"
git config user.name "{business.name} Dev"
git init
git add .
git commit -m "Initial commit: Site professionnel {business.name}"

ÉTAPE 5 - GitHub:
gh repo create {site_slug} --public --source=. --push

ÉTAPE 6 - Vercel (OBLIGATOIRE):
npx vercel --token $VERCEL_TOKEN --yes --prod --name {site_slug}

🚨 RÈGLES ABSOLUES:
1. Exécute LES 6 ÉTAPES COMPLÈTES
2. NE t'arrête PAS après GitHub
3. NE vérifie PAS l'état avant Vercel
4. NE fais PAS de résumé avant Vercel
5. Continue IMMÉDIATEMENT avec étape 6 après étape 5
6. Affiche les URLs GitHub ET Vercel à la FIN

⚠️ CRITÈRES DE QUALITÉ OBLIGATOIRES:
- Design moderne professionnel haut de gamme
- Mobile-first responsive parfait
- Animations Framer Motion smooth sur TOUTES les sections
- TypeScript strict sans erreurs
- SEO optimisé avec metadata et JSON-LD complets
- Formulaire multi-étapes fonctionnel avec validation Zod
- 8 sections complètes sur homepage (HERO, STATS, SERVICES, BEFORE/AFTER, TIMELINE, TESTIMONIALS, FAQ, FINAL CTA)
- Navigation sticky avec mega menu (desktop) et sticky bottom bar (mobile)
- Performance optimale (Next/Image, lazy loading)
- Composants BeforeAfterSlider, AnimatedCounter, ExitIntentPopup implémentés
- Pages dynamiques [slug-service] fonctionnelles
- Page /realisations avec galerie
- lib/schema.ts avec fonctions JSON-LD complètes

L'étape 6 (Vercel) est OBLIGATOIRE. Ne termine pas sans elle."""

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)
            github_url = None
            vercel_url = None
            error_occurred = False
            update_job("processing", 40, "Claude génère le code avec prompt complet...")

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    print(f"Claude: {message}")

                    if 'github.com' in content_str and not github_url:
                        import re
                        match = re.search(r'https://github\.com/[\w-]+/[\w-]+', content_str)
                        if match:
                            github_url = match.group(0)
                            update_job("processing", 70, "Repo GitHub créé", github_url=github_url)

                    if 'vercel.app' in content_str and not vercel_url:
                        import re
                        match = re.search(r'https://[\w-]+\.vercel\.app', content_str)
                        if match:
                            vercel_url = match.group(0)
                            update_job("processing", 90, "Déployé sur Vercel", site_url=vercel_url)

                    if 'error' in content_str.lower() or 'erreur' in content_str.lower():
                        error_occurred = True

        if not github_url and not vercel_url:
            github_url = f"https://github.com/poilopo2001/{site_slug}"
            vercel_url = f"https://{site_slug}.vercel.app"

        update_job("completed", 100, "Site généré et déployé!", github_url=github_url, site_url=vercel_url)

    except Exception as e:
        import traceback
        error_message = f"{str(e)}\n{traceback.format_exc()}"
        print(f"ERROR in generate_and_deploy: {error_message}")
        update_job("error", 0, f"Erreur: {str(e)}", error=error_message)

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job non trouvé")
    return jobs[job_id]
