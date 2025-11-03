# Backend API pour génération de sites avec Claude Code SDK
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

app = FastAPI(title="SaaS Generator v1")

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
    return {"status": "ok", "service": "SaaS Generator v1"}

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

        update_job("processing", 20, "Génération du site professionnel...")

        # Calcul de l'expérience
        current_year = 2024
        years_experience = current_year - business.year

        # PROMPT COMPLET avec toutes les spécifications
        prompt = f"""Génère le code source COMPLET d'un site web Next.js 14+ professionnel pour une entreprise locale B2B.

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
- Dossier: {site_dir}

🛠️ STACK TECHNIQUE OBLIGATOIRE:
- Next.js 14.2+ (App Router, Server Components par défaut, 'use client' si nécessaire)
- TypeScript (Mode Strict)
- Tailwind CSS 3.4.17+ (customisation complète)
- Framer Motion 12+ (animations scroll reveal et transitions)
- Lucide React (icônes)
- React Hook Form + Zod (formulaires validation)

📁 STRUCTURE FICHIERS COMPLÈTE:

projet/
├── app/
│   ├── layout.tsx              # Root layout avec Header, Footer, SEO
│   ├── page.tsx                # Homepage complète (8 sections)
│   ├── globals.css             # Tailwind + animations custom
│   ├── nos-services/page.tsx   # Page grille des services
│   ├── contact/page.tsx        # Page avec formulaire multi-étapes
│   ├── devis-gratuit/page.tsx  # Page de conversion
│   ├── mentions-legales/page.tsx
│   └── politique-confidentialite/page.tsx
├── components/
│   ├── ui/                     # Button, Input, Accordion
│   ├── layout/                 # Header, Footer, StickyBar
│   ├── sections/               # Hero, StatsBar, Testimonials, ProcessTimeline
│   └── forms/                  # ContactForm, MultiStepForm
├── lib/
│   ├── metadata.ts             # SEO centralisé
│   ├── schema.ts               # JSON-LD (LocalBusiness, Service, FAQPage)
│   └── constants.ts            # Données globales
├── public/
│   ├── sitemap.xml
│   └── robots.txt
├── package.json
├── tailwind.config.js
├── next.config.mjs
├── tsconfig.json
└── .gitignore

🎨 DESIGN SYSTEM:

Couleurs (tailwind.config.js):
- primary: '{business.primary_color}' (bleu professionnel)
- primary-700: '#103256' (hover/footer)
- primary-50: '#e6f0f9' (backgrounds)
- accent: '{business.secondary_color}' (orange conversion)
- accent-600: '#ff7519' (hover)

Typographie (Inter):
- H1 Hero: text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-extrabold
- H2 Section: text-3xl sm:text-4xl lg:text-5xl font-bold
- Body Large: text-lg sm:text-xl leading-relaxed

Composants Clés:
- .btn-primary: bg-primary hover:bg-primary-600 shadow-xl hover:scale-105
- .btn-accent: bg-accent hover:bg-accent-600 shadow-2xl (CTA conversion)
- .card-modern: bg-white rounded-2xl p-8 border border-gray-100 hover:shadow-3xl

Animations:
- TOUTES les sections: Framer Motion scroll reveal (opacity 0→1, y 50→0)
- Boutons: hover:scale-105 active:scale-95
- Transitions: transition-all duration-500 ease-in-out

📐 HOMEPAGE (app/page.tsx) - 8 SECTIONS:

1. HERO:
   - Fond image + Gradient Overlay
   - H1: USP locale chiffrée
   - 2 CTAs (Devis btn-accent, Réalisations btn-primary)
   - Social Proof immédiat

2. STATS BAR:
   - 4 Stats Cards (Projets, Années, Satisfaction, Délai)
   - Icônes Lucide, hover:scale-110

3. SERVICES GRID:
   - Grid 3 colonnes
   - ServiceCard: Image, Titre H3, 3 Bénéfices, CTAs

4. BEFORE/AFTER:
   - Slider interactif (3-4 projets)
   - Métriques chiffrées en badge

5. PROCESS TIMELINE:
   - Timeline verticale avec étapes numérotées
   - Fond gradient-primary
   - Animation staggerChildren

6. TESTIMONIALS:
   - Grid 3 colonnes
   - Citation, photo, nom, ville, 5 étoiles
   - hover:shadow-2xl hover:-translate-y-1

7. FAQ ACCORDION:
   - 5-6 questions fréquentes
   - Animation toggle smooth
   - Icône ChevronDown rotative

8. FINAL CTA:
   - Background image + Gradient
   - Formulaire simplifié (Nom, Tél, Code Postal)
   - Multi-CTA btn-xl

🧭 NAVIGATION:

Header (Client Component):
- Sticky avec réduction au scroll
- Menu horizontal desktop, Burger mobile
- Mega Menu Services (3 colonnes)
- CTA btn-accent "Devis Gratuit"

Sticky Bottom Bar (Mobile):
- 3 icônes: Appeler, Devis, Contact

🔍 SEO:

Metadata (lib/metadata.ts):
- Titres optimisés avec localisation
- Descriptions 150-160 caractères
- Keywords locaux

JSON-LD (lib/schema.ts):
- LocalBusiness (nom, adresse, téléphone, geo, horaires)
- Service (description, zone, prix range)
- FAQPage (questions/réponses)
- BreadcrumbList

Images:
- Utiliser <Image /> Next.js
- quality={{90}}
- priority={{true}} uniquement Hero
- Alt text SEO avec localisation

⚙️ ÉTAPES D'EXÉCUTION:

ÉTAPE 1 - Créer TOUS les fichiers:
- package.json (Next.js 14+, TypeScript, Tailwind, Framer Motion, Lucide, React Hook Form, Zod)
- tailwind.config.js (couleurs primary/accent complètes)
- next.config.mjs
- tsconfig.json
- app/layout.tsx (LocalBusiness JSON-LD)
- app/page.tsx (8 sections complètes)
- app/globals.css (Tailwind + animations)
- app/nos-services/page.tsx
- app/contact/page.tsx (MultiStepForm avec 4 étapes)
- app/devis-gratuit/page.tsx
- app/mentions-legales/page.tsx
- app/politique-confidentialite/page.tsx
- components/layout/Header.tsx (Client Component, Sticky)
- components/layout/Footer.tsx
- components/sections/Hero.tsx
- components/sections/StatsBar.tsx
- components/sections/ServicesGrid.tsx
- components/sections/ProcessTimeline.tsx
- components/sections/Testimonials.tsx
- components/ui/Button.tsx
- components/ui/Accordion.tsx
- components/forms/MultiStepForm.tsx (React Hook Form + Zod, 4 étapes)
- lib/metadata.ts
- lib/schema.ts (fonctions generateLocalBusinessSchema, generateServiceSchema, generateFAQSchema)
- lib/constants.ts
- public/sitemap.xml
- public/robots.txt
- .gitignore
- README.md

ÉTAPE 2 - Installer: cd {site_dir} && npm install

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

⚠️ CRITÈRES DE QUALITÉ:
- Design moderne professionnel haut de gamme
- Mobile-first responsive parfait
- Animations Framer Motion smooth sur toutes les sections
- TypeScript strict sans erreurs
- SEO optimisé avec metadata et JSON-LD complets
- Formulaire multi-étapes fonctionnel avec validation Zod
- 8 sections complètes sur homepage
- Navigation sticky avec mega menu
- Performance optimale (Next/Image, lazy loading)

L'étape 6 (Vercel) est OBLIGATOIRE. Ne termine pas sans elle."""

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)
            github_url = None
            vercel_url = None
            error_occurred = False
            update_job("processing", 40, "Claude génère le code...")

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

                    if 'error' in content_str.lower() or 'failed' in content_str.lower():
                        error_occurred = True

                if hasattr(message, 'subtype'):
                    if message.subtype == 'success':
                        break
                    elif message.subtype == 'error':
                        error_occurred = True
                        break

            if error_occurred and not github_url:
                raise Exception("Erreur lors de la génération")

            final_site_url = vercel_url if vercel_url else github_url
            update_job("completed", 100, "Site généré et déployé !", github_url=github_url, site_url=final_site_url)

    except Exception as e:
        import traceback
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        update_job("error", 0, f"Erreur: {str(e)}", error=str(e))

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job non trouvé")
    return jobs[job_id]

@app.get("/api/jobs")
async def list_jobs():
    return {"jobs": list(jobs.values())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
