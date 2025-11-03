"""
Code Generator Agent - Génère le code Next.js complet du site
"""
from typing import Dict, Any
from datetime import datetime


class CodeGeneratorAgent:
    """Agent spécialisé dans la génération de code Next.js 14+ avec App Router"""

    @staticmethod
    def get_prompt(business: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """
        Génère le prompt complet pour la création du site Next.js

        Args:
            business: Dictionnaire avec les données de l'entreprise
            site_slug: Slug du site (ex: "plomberie-luxembourg")
            site_dir: Chemin du répertoire de sortie

        Returns:
            Le prompt complet pour Claude Code SDK
        """
        years_experience = datetime.now().year - business.get("year", datetime.now().year)

        return f"""Générer le code source complet et fonctionnel d'un site web Next.js 14+ (App Router) pour une entreprise locale de services B2B. Le site doit être mobile-first, ultra-rapide, SEO-optimisé localement et présenter un design professionnel moderne et haut de gamme (minimaliste, axé sur les couleurs primaires/accent, avec des animations subtiles et des composants réutilisables).

📋 INFORMATIONS ENTREPRISE:

VARIABLES À UTILISER DANS LE CODE:
- [NOM_ENTREPRISE] = "{business.get('name', '')}"
- [LOCATION] = "{business.get('location', '')}"
- [PHONE] = "{business.get('phone', '')}"
- [EMAIL] = "{business.get('email', '')}"
- [ANNEE] = "{business.get('year', '')}"
- [EXPERIENCE] = "{years_experience} ans"
- [DOMAIN_URL] = "{business.get('domain_url') or f'https://{site_slug}.vercel.app'}"

ADRESSE PHYSIQUE (LocalBusiness Schema):
- Rue: "{business.get('street', '')}"
- Code Postal: "{business.get('postal_code', '')}"
- Ville: "{business.get('city', '')}"
- Pays: "{business.get('country', 'Luxembourg')}"
- Horaires: "{business.get('hours', 'Lundi-Vendredi 8h-18h')}"

SERVICES ET POSITIONNEMENT:
- Services: {business.get('services', '')}
- USP/Positionnement: {business.get('positioning', '')}

DESIGN:
- Couleur Primary: {business.get('primary_color', '#1a5490')}
- Couleur Accent: {business.get('secondary_color', '#ff8c42')}

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

Primary (Base): {business.get('primary_color', '#1a5490')} - Bleu professionnel, autoritaire, confiance.
Primary-700: #103256 - Teinte foncée pour hover/footer.
Primary-50: #e6f0f9 - Teinte très claire pour backgrounds subtils.
Accent (Base): {business.get('secondary_color', '#ff8c42')} - Orange énergique, conversion, éléments clés (CTAs).
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

.card-modern: bg-white / rounded-2xl / p-8. Bordure subtile: border border-gray-100. Effet de survol: hover:shadow-2xl hover:border-accent. Utilisé pour services, témoignages, étapes.

Glassmorphism: bg-white/10 backdrop-blur-md border border-white/20. Utilisé pour les popups et les éléments transparents sur des images de fond.

2.4 Animations Framer Motion & CSS

TOUTES les sections qui entrent dans le viewport DOIVENT utiliser Framer Motion pour un scroll reveal subtil:
initial: {{{{ opacity: 0, y: 50 }}}}, whileInView: {{{{ opacity: 1, y: 0 }}}}, transition: {{{{ duration: 0.8 }}}}

Animation - animate-fadeInUp: Titres et blocs de texte majeurs. Staggering (staggerChildren) pour les listes et les CTA multiples.
Animation - animate-float: Icônes ou éléments décoratifs dans la Hero Section. Mouvement lent ease-in-out infinite.
Animation - animate-pulse-glow: L'indicateur de nouvelle notification ou le bouton de téléphone sticky. Effet de halo autour d'un CTA.
Transitions: transition-all duration-500 ease-in-out sur tous les hover.

[... Suite du prompt très long - incluant toutes les parties 3 à 6 ...]

⚙️ ÉTAPES D'EXÉCUTION OBLIGATOIRES:

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
