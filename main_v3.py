"""
SaaS Generator v3 - FastAPI Backend with Specialized Agents
Uses github-publisher and vercel-deployer agents for deployment automation
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import anthropic
import os
import json
import asyncio
from datetime import datetime
import re

app = FastAPI(title="SaaS Generator v3 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Job tracking
jobs: Dict[str, Dict[str, Any]] = {}

class BusinessData(BaseModel):
    description: str

class SiteGenerationRequest(BaseModel):
    name: str
    location: str
    phone: str
    email: str
    year: int
    services: str
    positioning: str
    street: str
    postal_code: str
    city: str
    country: str = "Luxembourg"
    hours: str = "Lundi-Vendredi 8h-18h"
    primary_color: str = "#1a5490"
    secondary_color: str = "#ff8c42"
    domain_url: Optional[str] = None

# Endpoint 1: AI Pre-fill (unchanged from v2)
@app.post("/api/prefill")
async def prefill_form(data: BusinessData):
    """Analyse la description et pré-remplit le formulaire avec l'IA"""
    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

        prompt = f"""Analyse cette description d'entreprise et extrais UNIQUEMENT les informations concrètes mentionnées. Si une information n'est PAS explicitement mentionnée, utilise null.

Description: {data.description}

Réponds UNIQUEMENT avec un JSON valide dans ce format exact (sans markdown, sans texte avant ou après):
{{
  "name": "nom exact de l'entreprise ou null",
  "location": "ville/pays ou null",
  "phone": "numéro de téléphone exact ou null",
  "email": "email exact ou null",
  "year": année de création (nombre) ou null,
  "services": "liste des services mentionnés ou null",
  "positioning": "positionnement/USP mentionné ou null",
  "street": "adresse rue exacte ou null",
  "postal_code": "code postal exact ou null",
  "city": "ville exacte ou null",
  "country": "pays exact ou null",
  "hours": "horaires exacts mentionnés ou null"
}}

RÈGLES STRICTES:
- N'invente AUCUNE information
- Si l'information n'est pas dans la description, mets null
- Les valeurs null doivent être sans guillemets
- Le year doit être un nombre ou null (sans guillemets)
- Réponds UNIQUEMENT avec le JSON, rien d'autre"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        response_text = response_text.strip()

        parsed_data = json.loads(response_text)

        # Convertir les null en chaînes vides pour éviter les erreurs frontend
        for key in parsed_data:
            if parsed_data[key] is None:
                parsed_data[key] = ""

        return {
            "success": True,
            "data": parsed_data
        }
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Erreur parsing JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# Endpoint 2: Generate Site with Specialized Agents
@app.post("/api/generate")
async def generate_site(request: SiteGenerationRequest, background_tasks: BackgroundTasks):
    """Lance la génération d'un site avec agents spécialisés pour GitHub et Vercel"""

    job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    site_slug = f"{request.name.lower().replace(' ', '-')}-{request.city.lower()}"

    jobs[job_id] = {
        "id": job_id,
        "status": "pending",
        "progress": 0,
        "message": "Initialisation...",
        "created_at": datetime.now().isoformat(),
        "site_slug": site_slug
    }

    background_tasks.add_task(run_generation_with_agents, job_id, request, site_slug)

    return {
        "success": True,
        "job_id": job_id,
        "message": "Génération démarrée avec agents spécialisés"
    }

async def run_generation_with_agents(job_id: str, business: SiteGenerationRequest, site_slug: str):
    """Processus de génération en 4 phases: 1) Code Generation 2) Validation 3) GitHub Publisher 4) Vercel Deployer"""

    def update_job(status: str, progress: int, message: str, **kwargs):
        jobs[job_id].update({
            "status": status,
            "progress": progress,
            "message": message,
            "updated_at": datetime.now().isoformat(),
            **kwargs
        })

    try:
        update_job("processing", 10, "Phase 1/4: Génération du code Next.js complet...")

        # PHASE 1: Code Generation avec Claude Code SDK
        site_dir = f"/tmp/generated-sites/{site_slug}"
        years_experience = datetime.now().year - business.year

        # Créer le dossier du site AVANT d'initialiser ClaudeCodeOptions
        os.makedirs(site_dir, exist_ok=True)

        # Import Claude Code SDK
        from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions

        options = ClaudeCodeOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=["Write", "Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"GH_TOKEN": os.getenv("GITHUB_TOKEN", ""), "VERCEL_TOKEN": os.getenv("VERCEL_TOKEN", "")}
        )

        # Prompt complet de génération (identique à v2)
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

Animation - animate-fadeInUp: Titres et blocs de texte majeurs. Staggering (staggerChildren) pour les listes et les CTA multiples.
Animation - animate-float: Icônes ou éléments décoratifs dans la Hero Section. Mouvement lent ease-in-out infinite.
Animation - animate-pulse-glow: L'indicateur de nouvelle notification ou le bouton de téléphone sticky. Effet de halo autour d'un CTA.
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

Header: <Breadcrumbs> obligatoire.
Hero Spécifique: Image hero + H1, sous-titre, 3 points forts (ex: Performance, Économie, Garantie). CTA btn-accent.
Section Problème/Solution/Bénéfices: Contenu structuré. Titres H2, liste à puces avec icônes.
Galerie Photos/Études de Cas: Grid 3 colonnes de réalisations spécifiques à ce service.
Pricing (Transparent): Section H2 titrée "Prix et Estimation". Affichage d'une range de prix (ex: 2300€ - 3500€/m²) avec explication des facteurs de variation.
Trust Badges / Certifications: 4 badges (ex: RGE, Garantie Décennale) en grid.
FAQ Spécifique: <Accordion> avec 4-5 questions/réponses spécifiques au service.
CTA Final: Section minimaliste avec un unique bouton btn-accent.

3.3 PAGE CONTACT (/contact/page.tsx)

Titre: H1 "Contactez-nous | Réponse Garantie en 24h".
Formulaire Multi-Étapes (OBLIGATOIRE): Utilise le composant <MultiStepForm>.
Logique: 4 étapes avec progression visuelle (barre/indicateur). Validation Zod à chaque étape.
Étape 1: Type de Projet (Radio Buttons Visuels: Extension, Isolation, Rénovation).
Étape 2: Caractéristiques (Surface m², Budget Range - Sliders).
Étape 3: Timing (Quand souhaitez-vous commencer? - Select).
Étape 4: Coordonnées (Nom, Prénom, Téléphone, Email, Code Postal, RGPD Checkbox).
Informations Contact: Grid 2 colonnes à côté du formulaire.
Coordonnées (Adresse, Email, Téléphone - cliquables).
Horaires d'ouverture.
Carte: Google Maps embed (iframe ou composant Map si librairie légère).

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

État géré par: const [isSticky, setIsSticky] = useState(false) avec useEffect scroll listener
Menu mobile: const [isOpen, setIsOpen] = useState(false)

4.2 Sticky Bottom Bar (Mobile)
OBLIGATOIRE pour la conversion mobile. Barre fixe en bas de l'écran avec 3 icônes/liens visibles:
- Appeler (Icône Phone cliquable)
- Devis (Icône Calculator cliquable, btn-accent stylisé)
- Simulateur/Contact (Icône Mail ou Zap)

4.3 Exit Intent Popup (components/forms/ExitIntentPopup.tsx)
Logique de déclenchement:
Desktop: Écouteur d'événement mouseleave qui se déclenche lorsque le curseur quitte le haut de la fenêtre.
Mobile: Déclenchement au défilement inversé rapide (scroll up) ou après 60 secondes.
Contenu: Offre d'urgence (ex: "Ne partez pas! Votre devis gratuit sous 48h expire!"). Formulaire minimaliste (Email + Tél).

🔍 PARTIE 5 : SEO & PERFORMANCE AVANCÉS

5.1 Metadata & SEO Local (lib/metadata.ts)
Toutes les pages DOIVENT utiliser des métadonnées centralisées, injectant les variables locales.

export const PAGE_METADATA = {{
  home: {{
    title: "Extension Combles {business.city} | Agrandissement +30m² | Devis 48h",
    description: "Expert extension combles {business.city} depuis {years_experience} ans. Gagnez 30-50m² habitables. Devis gratuit 48h. Garantie décennale. Prix compétitifs.",
    keywords: ["extension combles {business.city}", "agrandissement maison {business.city}", "prix extension"],
    canonical: "{business.domain_url or f'https://{site_slug}.vercel.app'}/"
  }}
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

IMPORTANT: Après avoir terminé les 3 étapes, ARRÊTE-TOI. NE fais PAS de commit git, NE crée PAS de repo GitHub, NE déploie PAS sur Vercel. Ces étapes seront gérées par des agents spécialisés."""

        # Execute code generation
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)
            update_job("processing", 40, "Code généré, build en cours...")

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    print(f"Claude Code Generation: {message}")

        # PHASE 2: Validation & Auto-Fix Loop (max 3 attempts)
        max_retry_attempts = 3
        validation_passed = False

        for attempt in range(1, max_retry_attempts + 1):
            update_job("processing", 50 + (attempt - 1) * 2, f"Phase 2/4: Validation qualité (tentative {attempt}/{max_retry_attempts})...")

            # PHASE 2a: Site Validation with site-validator-pro agent
            validation_prompt = f"""Tu es l'agent site-validator-pro. Valide ce site Next.js généré pour garantir sa production-readiness.

Projet à valider: {site_dir}

Exécute ton workflow complet de validation multi-agent:
1. Structure Validation (files, folders, Next.js conventions)
2. UI/CSS Validation (Tailwind, responsive, design system)
3. Image Validation (Next/Image usage, optimization, alt text)
4. Functionality Validation (build success, TypeScript errors, runtime)
5. Content Validation (SEO metadata, JSON-LD, accessibility)
6. Performance Validation (Lighthouse scores, best practices)

Génère un rapport détaillé avec:
- Liste EXACTE des erreurs trouvées (fichier:ligne)
- Sévérité de chaque erreur (CRITICAL, HIGH, MEDIUM, LOW)
- Indique clairement SAFE TO DEPLOY ou FAILED"""

            options_validation = ClaudeCodeOptions(
                model="claude-haiku-4-5-20251001",
                allowed_tools=["Read", "Grep", "Glob", "Bash"],
                permission_mode="acceptEdits",
                cwd=site_dir
            )

            validation_report = ""
            has_critical_errors = False

            async with ClaudeSDKClient(options=options_validation) as client:
                await client.query(validation_prompt)

                async for message in client.receive_messages():
                    if hasattr(message, 'content'):
                        content_str = str(message.content)
                        print(f"Site Validator Pro (Attempt {attempt}): {message}")
                        validation_report += content_str

                        # Check for validation status
                        if 'SAFE TO DEPLOY' in content_str or 'PASSED' in content_str:
                            validation_passed = True
                            update_job("processing", 56, f"✅ Validation réussie (tentative {attempt}) - Site production-ready")
                        elif 'CRITICAL' in content_str or 'FAILED' in content_str:
                            has_critical_errors = True

            # If validation passed, exit the loop
            if validation_passed:
                break

            # If validation failed and we have attempts left, try to auto-fix
            if has_critical_errors and attempt < max_retry_attempts:
                update_job("processing", 56 + attempt, f"🔧 Phase 2.5: Correction automatique des erreurs (tentative {attempt})...")

                # PHASE 2.5: Auto-Fix with Claude
                fix_prompt = f"""Tu as généré un site Next.js qui présente des erreurs de validation. Tu dois CORRIGER tous les problèmes détectés.

RAPPORT DE VALIDATION (Tentative {attempt}):
{validation_report}

RÉPERTOIRE DU PROJET: {site_dir}

INSTRUCTIONS DE CORRECTION:
1. Analyse TOUTES les erreurs listées dans le rapport
2. Pour chaque erreur CRITICAL ou HIGH:
   - Localise le fichier concerné
   - Corrige l'erreur (TypeScript, imports, composants manquants, etc.)
   - Vérifie que la correction n'introduit pas de nouveaux problèmes
3. Après toutes les corrections, relance: cd {site_dir} && npm run build
4. Vérifie que le build réussit sans erreurs

FOCUS PRIORITAIRE:
- Erreurs TypeScript (types manquants, imports incorrects)
- Erreurs de build (modules not found, syntax errors)
- Composants manquants ou mal implémentés
- Problèmes de configuration (next.config.js, tailwind.config.js)

Corrige TOUS les fichiers nécessaires, puis confirme que le build passe."""

                options_fix = ClaudeCodeOptions(
                    model="claude-haiku-4-5-20251001",
                    allowed_tools=["Write", "Read", "Edit", "Bash"],
                    permission_mode="acceptEdits",
                    cwd=site_dir
                )

                async with ClaudeSDKClient(options=options_fix) as client:
                    await client.query(fix_prompt)

                    async for message in client.receive_messages():
                        if hasattr(message, 'content'):
                            print(f"Auto-Fix (Attempt {attempt}): {message}")

                update_job("processing", 57 + attempt, f"🔄 Re-validation après corrections (tentative {attempt})...")
                # Loop will automatically re-validate in next iteration

            elif has_critical_errors and attempt >= max_retry_attempts:
                # Exhausted all retry attempts
                update_job("failed", 58, f"❌ Échec après {max_retry_attempts} tentatives - Issues critiques non résolues")
                raise Exception(f"Validation failed after {max_retry_attempts} attempts. Last report:\n{validation_report}")

        if not validation_passed:
            # If validation didn't explicitly pass but no critical errors, treat as warning
            update_job("processing", 58, "⚠️ Validation complétée avec warnings - Poursuite déploiement")

        update_job("processing", 60, "Phase 3/4: Publication GitHub avec agent spécialisé...")

        # PHASE 3: GitHub Publication with github-publisher agent
        github_payload = {
            "projectPath": site_dir,
            "repoName": site_slug,
            "businessData": {
                "nom": business.name,
                "ville": business.city,
                "secteur": business.services.split(',')[0].strip() if business.services else "services"
            },
            "githubConfig": {
                "username": "poilopo2001",
                "email": "sebastien.poletto@gmail.com",
                "visibility": "public"
            }
        }

        github_prompt = f"""Tu es l'agent github-publisher. Publie ce projet sur GitHub avec la configuration suivante:

{json.dumps(github_payload, indent=2, ensure_ascii=False)}

Exécute TOUTES les phases de ton workflow (1-6) de manière complète et systématique. Retourne l'URL du repository GitHub créé."""

        options_github = ClaudeCodeOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=["Bash", "Read", "Edit"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"GH_TOKEN": os.getenv("GITHUB_TOKEN", "")}
        )

        github_url = None
        async with ClaudeSDKClient(options=options_github) as client:
            await client.query(github_prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    print(f"GitHub Publisher: {message}")

                    if 'github.com' in content_str and not github_url:
                        match = re.search(r'https://github\.com/[\w-]+/[\w-]+', content_str)
                        if match:
                            github_url = match.group(0)
                            update_job("processing", 75, "Repository GitHub créé", github_url=github_url)

        if not github_url:
            raise Exception("GitHub repository creation failed - no URL returned")

        update_job("processing", 80, "Phase 4/4: Déploiement Vercel avec agent spécialisé...")

        # PHASE 4: Vercel Deployment with vercel-deployer agent
        vercel_payload = {
            "projectPath": site_dir,
            "projectName": site_slug,
            "businessData": {
                "nom": business.name,
                "ville": business.city,
                "siteUrl": business.domain_url or f"https://{site_slug}.vercel.app"
            },
            "githubRepo": github_url.replace("https://github.com/", ""),
            "vercelConfig": {
                "customDomain": business.domain_url.replace("https://", "").replace("http://", "") if business.domain_url else None,
                "framework": "nextjs",
                "envVars": {
                    "NEXT_PUBLIC_SITE_URL": business.domain_url or f"https://{site_slug}.vercel.app",
                    "NEXT_PUBLIC_CONTACT_EMAIL": business.email
                }
            }
        }

        vercel_prompt = f"""Tu es l'agent vercel-deployer. Déploie ce projet Next.js sur Vercel avec la configuration suivante:

{json.dumps(vercel_payload, indent=2, ensure_ascii=False)}

Exécute TOUTES les phases de ton workflow (1-9) de manière complète et systématique. Retourne l'URL Vercel de production."""

        options_vercel = ClaudeCodeOptions(
            model="claude-haiku-4-5-20251001",
            allowed_tools=["Bash", "Read", "Edit"],
            permission_mode="acceptEdits",
            cwd=site_dir,
            env={"VERCEL_TOKEN": os.getenv("VERCEL_TOKEN", "")}
        )

        vercel_url = None
        async with ClaudeSDKClient(options=options_vercel) as client:
            await client.query(vercel_prompt)

            async for message in client.receive_messages():
                if hasattr(message, 'content'):
                    content_str = str(message.content)
                    print(f"Vercel Deployer: {message}")

                    if 'vercel.app' in content_str and not vercel_url:
                        match = re.search(r'https://[\w-]+\.vercel\.app', content_str)
                        if match:
                            vercel_url = match.group(0)
                            update_job("processing", 95, "Site déployé sur Vercel", site_url=vercel_url)

        # Final status
        if github_url and vercel_url:
            update_job("completed", 100, "Génération terminée avec succès!",
                      github_url=github_url,
                      site_url=vercel_url)
        elif github_url:
            update_job("completed", 100, "Code publié sur GitHub (Vercel manuel)",
                      github_url=github_url,
                      site_url=f"https://{site_slug}.vercel.app (déployer manuellement)")
        else:
            update_job("completed", 100, "Code généré (publication manuelle requise)",
                      message="Le code est prêt dans " + site_dir)

    except Exception as e:
        update_job("failed", 0, f"Erreur: {str(e)}")
        print(f"Generation error: {str(e)}")

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """Récupère le statut d'une génération"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job non trouvé")
    return jobs[job_id]

@app.get("/api/jobs")
async def list_jobs():
    """Liste tous les jobs"""
    return {"jobs": list(jobs.values())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
