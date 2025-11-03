Générer le code source complet et fonctionnel d'un site web Next.js 14+ (App Router) pour une entreprise locale de services B2B. Le site doit être mobile-first, ultra-rapide, SEO-optimisé localement et présenter un design professionnel moderne et haut de gamme (minimaliste, axé sur les couleurs primaires/accent, avec des animations subtiles et des composants réutilisables).
🛠️ PARTIE 1 : ARCHITECTURE TECHNIQUE & CONFIGURATION
1.1 Stack Technologique OBLIGATOIRE
Élément	Spécification
Framework	Next.js 14.2+ (App Router, Server Components par défaut, 'use client' si nécessaire)
Langage	TypeScript (Mode Strict)
Styling	Tailwind CSS 3.4.17+ (avec customisation complète des couleurs/thèmes)
Animations	Framer Motion 12+ (pour les transitions page, scroll reveal, et micro-interactions)
Icônes	Lucide React
Images	Next/Image (avec optimisation et gestion priority)
Formulaires	React Hook Form (pour la logique d'état) + Zod (pour la validation des schémas)
Deployment	Vercel (Production Ready)
1.2 Structure Fichiers Complète
La structure doit inclure tous les éléments pour le SEO, la logique et le contenu, en utilisant des Server Components par défaut pour les pages et des Client Components pour les interactivité (Formulaires, Header, Popups).
code
Code
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
Élément	Couleur Hex	Description
Primary (Base)	#1a5490	Bleu professionnel, autoritaire, confiance.
Primary-700	#103256	Teinte foncée pour hover/footer.
Primary-50	#e6f0f9	Teinte très claire pour backgrounds subtils.
Accent (Base)	#ff8c42	Orange énergique, conversion, éléments clés (CTAs).
Accent-600	#ff7519	Teinte foncée pour hover/active.
Neutral	gray	Utiliser les teintes gray-50 à gray-900 de Tailwind.
2.2 Typographie Système
Police Inter avec une échelle typographique modulaire et lisible.
Élément	Classe Tailwind (Custom)	Détail
H1 (Hero)	text-hero	text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-extrabold leading-none
H2 (Section)	text-h2	text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight
H3 (Titre Card)	text-h3	text-2xl sm:text-3xl font-bold
Body Large	text-body-large	text-lg sm:text-xl leading-relaxed (pour sous-titres/intro)
Body	text-body	text-base leading-relaxed
2.3 Composants de Design Clés (Classes Utilitaires)
Composant	Description du Design & Classes	Logique UX
.btn-primary	bg-primary / text-white. hover:bg-primary-600. Effet d'Ombre Léger: shadow-xl. Micro-interaction: hover:scale-105 active:scale-95.	Le CTA principal pour la marque.
.btn-accent	OBLIGATOIRE pour la Conversion. bg-accent / text-white. hover:bg-accent-600. Effet de "Glow": shadow-accent/40 shadow-2xl.	Le CTA le plus visible (Devis Gratuit).
.card-modern	bg-white / rounded-2xl / p-8. Bordure subtile: border border-gray-100. Effet de survol: hover:shadow-3xl hover:border-accent.	Utilisé pour services, témoignages, étapes.
Glassmorphism	bg-white/10 backdrop-blur-md border border-white/20.	Utilisé pour les popups et les éléments transparents sur des images de fond.
2.4 Animations Framer Motion & CSS
TOUTES les sections qui entrent dans le viewport DOIVENT utiliser Framer Motion pour un scroll reveal subtil (initial: { opacity: 0, y: 50 }, whileInView: { opacity: 1, y: 0 }, transition: { duration: 0.8 }).
Animation	Usage	Spécificité
animate-fadeInUp	Titres et blocs de texte majeurs.	Staggering (staggerChildren) pour les listes et les CTA multiples.
animate-float	Icônes ou éléments décoratifs dans la Hero Section.	Mouvement lent ease-in-out infinite.
animate-pulse-glow	L'indicateur de nouvelle notification ou le bouton de téléphone sticky.	Effet de halo autour d'un CTA.
Transitions	transition-all duration-500 ease-in-out sur tous les hover.	
📐 PARTIE 3 : STRUCTURE PAGES DÉTAILLÉE (UX & LOGIQUE)
3.1 HOMEPAGE (/)
Le fichier app/page.tsx doit être un Client Component ('use client') pour gérer les états des tabs, FAQ et animations.
Section	Titre & Objectif	Design & Logique de Composant
1. HERO	H1: USP locale et chiffrée. (Conversion)	Fond image haute résolution + Gradient Overlay (bg-gradient-hero). Shapes animées (Blob) derrière le texte. Texte centré sur la promesse de valeur. 2 CTAs (Primaire: Devis, Secondaire: Réalisations). Social Proof (étoiles, expérience chiffrée) visible immédiatement.
2. STATS BAR	Chiffres Clés (Trust Signal)	Section bg-white qui "monte" visuellement au-dessus de la Hero. 4 Cards/Stats (Projets, Années, Satisfaction, Délai Devis). Icônes Lucide. Effet Micro-interaction: hover:scale-110 sur chaque stat.
3. SERVICES GRID	Présentation des Offres (Découverte)	Grid 3 colonnes (lg:grid-cols-3). Utilise le composant <ServiceCard>. Design: Image aspect-[4/3] avec survol group-hover:scale-110, Titre H3, Liste de 3 Bénéfices avec CheckCircle2 (accent), CTA "En Savoir Plus" (btn-secondary) + "Devis" (btn-accent).
4. BEFORE/AFTER (Projets)	Preuve Visuelle (Crédibilité)	Utilise le composant <BeforeAfterSlider>: Slider interactif (drag-to-compare) pour 3-4 projets. Onglets cliquables pour changer de projet. Métrique Chiffrée (ex: "+45m²") en badge.
5. PROCESS TIMELINE	Explication du Processus (Transparence)	Design de Timeline Verticale Sophistiqué. Fond gradient-primary. Étapes numérotées (1, 2, 3...) avec une ligne de connexion verticale (CSS/Tailwind). Chaque étape est un <ProcessStep> avec un titre H3 et description, animée en staggerChildren.
6. TESTIMONIALS	Avis Clients (Réassurance)	Grid 3 colonnes. Utilise le composant <TestimonialCard>. Design: Citation en italique, photo (ou initiales), Nom, Ville, Rating 5 étoiles (Accent). Citation visible: 50-70 mots. hover:shadow-2xl hover:-translate-y-1.
7. FAQ ACCORDION	Levier de Friction (SEO & UX)	Utilise le composant <Accordion>. Design card-modern individuel. Animation de toggle du contenu (smooth max-height transition). Icône ChevronDown rotative à l'ouverture. Contient les 5-6 questions les plus fréquentes.
8. FINAL CTA	Conversion Finale (Closing)	Background image pleine largeur avec Gradient gradient-accent overlay. Titre H1 impactant (ex: "Il est temps de concrétiser votre projet"). Multi-CTA : Bouton btn-xl ("Obtenir mon Devis Gratuit") + Icône Phone cliquable + Formulaire simplifié (Nom, Tél, Code Postal).
3.2 PAGE SERVICE INDIVIDUELLE (/[slug-service]/page.tsx)
Header : <Breadcrumbs> obligatoire.
Hero Spécifique : Image hero + H1, sous-titre, 3 points forts (ex: Performance, Économie, Garantie). CTA btn-accent.
Section Problème/Solution/Bénéfices : Contenu structuré. Titres H2, liste à puces avec icônes.
Galerie Photos/Études de Cas : Grid 3 colonnes de réalisations spécifiques à ce service.
Pricing (Transparent) : Section H2 titrée "Prix et Estimation". Affichage d'une range de prix (ex: 2300€ - 3500€/m²) avec explication des facteurs de variation.
Trust Badges / Certifications : 4 badges (ex: RGE, Garantie Décennale) en grid.
FAQ Spécifique : <Accordion> avec 4-5 questions/réponses spécifiques au service.
CTA Final : Section minimaliste avec un unique bouton btn-accent.
3.3 PAGE CONTACT (/contact/page.tsx)
Titre : H1 "Contactez-nous | Réponse Garantie en 24h".
Formulaire Multi-Étapes (OBLIGATOIRE) : Utilise le composant <MultiStepForm>.
Logique : 4 étapes avec progression visuelle (barre/indicateur). Validation Zod à chaque étape.
Étape 1 : Type de Projet (Radio Buttons Visuels : Extension, Isolation, Rénovation).
Étape 2 : Caractéristiques (Surface m², Budget Range - Sliders).
Étape 3 : Timing (Quand souhaitez-vous commencer ? - Select).
Étape 4 : Coordonnées (Nom, Prénom, Téléphone, Email, Code Postal, RGPD Checkbox).
Informations Contact : Grid 2 colonnes à côté du formulaire.
Coordonnées (Adresse, Email, Téléphone - cliquables).
Horaires d'ouverture.
Carte : Google Maps embed (iframe ou composant Map si librairie légère).
🧭 PARTIE 4 : NAVIGATION & UX AVANCÉE
4.1 Header (components/layout/Header.tsx)
DOIT ÊTRE un Client Component.
Élément	Desktop (≥1024px)	Mobile (<1024px)	Logique d'État
Général	Sticky Header (réduit en taille au scroll).	Sticky Bottom Bar (voir ci-dessous).	const [isSticky, setIsSticky] = useState(false) géré par useEffect avec scroll listener.
Navigation	Menu horizontal avec hover:text-accent.	<BurgerMenu> toggle pour ouvrir un overlay plein écran.	const [isOpen, setIsOpen] = useState(false)
Mega Menu	Menu Services : S'ouvre au survol. Structure 3 colonnes (Liens Services, Liens Infos/Guides, CTA Visuel Fort avec image/gradient).	Les services sont listés dans l'overlay.	
CTA Principal	btn-accent "Devis Gratuit" toujours visible à droite.	Déplacé dans l'overlay et la Sticky Bottom Bar.	
4.2 Sticky Bottom Bar (Mobile)
OBLIGATOIRE pour la conversion mobile. Barre fixe en bas de l'écran avec 3 icônes/liens visibles :
Appeler (Icône Phone cliquable).
Devis (Icône Calculator cliquable, btn-accent stylisé).
Simulateur/Contact (Icône Mail ou Zap).
4.3 Exit Intent Popup (components/forms/ExitIntentPopup.tsx)
Logique de déclenchement :
Desktop : Écouteur d'événement mouseleave qui se déclenche lorsque le curseur quitte le haut de la fenêtre.
Mobile : Déclenchement au défilement inversé rapide (scroll up) ou après 60 secondes.
Contenu : Offre d'urgence (ex: "Ne partez pas ! Votre devis gratuit sous 48h expire !"). Formulaire minimaliste (Email + Tél).
🔍 PARTIE 5 : SEO & PERFORMANCE AVANCÉS
5.1 Metadata & SEO Local (lib/metadata.ts)
Toutes les pages DOIVENT utiliser des métadonnées centralisées, injectant les variables locales.
code
TypeScript
// lib/metadata.ts
export const PAGE_METADATA = {
  home: {
    title: "Extension Combles [LOCATION] | Agrandissement +30m² | Devis 48h",
    description: "Expert extension combles [LOCATION] depuis [ANNEE] ans. Gagnez 30-50m² habitables. Devis gratuit 48h. Garantie décennale. Prix compétitifs.",
    keywords: ["extension combles [LOCATION]", "agrandissement maison [LOCATION]", "prix extension"],
    canonical: "https://domain.com/"
  },
  // ... autres pages
}

// app/page.tsx ou layout.tsx
import { PAGE_METADATA } from '@/lib/metadata';
export const metadata: Metadata = PAGE_METADATA.home;
5.2 Structured Data (JSON-LD)
Le fichier lib/schema.ts DOIT contenir des fonctions générant les schémas suivants.
LocalBusiness (dans app/layout.tsx) : Incluant le nom, l'adresse, les coordonnées (telephone), le geo (latitude/longitude), et les openingHours.
Service (dans chaque page de service) : Décrivant le service, la zone, et le prix range.
FAQPage (dans les pages avec Accordion) : Représentant les questions/réponses.
BreadcrumbList (dans <Breadcrumbs.tsx>) : Pour le fil d'Ariane.
5.3 Images Optimisées
Toutes les images DOIVENT utiliser <Image /> de Next.js.
Qualité : quality={90}.
Lazy Loading : priority={true} uniquement pour la Hero Image. Toutes les autres images doivent être en lazy loading par défaut.
Alt Text : Description SEO-friendly incluant la localisation (ex: "Isolation combles achevé à [Ville]").
⚙️ PARTIE 6 : INSTRUCTIONS DE GÉNÉRATION FINALES
6.1 Directives de Codage
Commencer par la structure des dossiers, package.json, tailwind.config.js et next.config.mjs.
Créer les composants de layout (Header.tsx, Footer.tsx) avec la logique d'état (sticky, mobile menu).
Développer la app/page.tsx en utilisant les composants de section réutilisables décrits en P3.
Implémenter le <MultiStepForm> dans contact/page.tsx avec la logique de React Hook Form/Zod.
Pour les animations, utiliser la syntaxe de Framer Motion sur les éléments clés et les classes CSS (animate-fadeInUp, delay-X).
6.2 Customisation Requise (Variables Agnostiques)
Le site généré doit utiliser les placeholders suivants, qui rendent le code agnostique :
Variable	Description	Emplacement Principal
[NOM_ENTREPRISE]	Le nom de l'entreprise locale.	Metadata, Header, Footer, LocalBusiness Schema
[LOCATION]	Ville/Pays cible (ex: Luxembourg).	Metadata, Titres H1/H2, Alt Images, Schema
[PHONE]	Numéro de téléphone cliquable.	Header, Footer, Sticky Bar, Schema
[EMAIL]	Adresse e-mail de contact.	Footer, Contact Form, Schema
[ANNEE]	Année de début d'activité (pour l'expérience).	Hero Section, Footer
[SERVICES_LIST]	La liste des services de l'entreprise.	Navigation, Services Grid
[UNSPLASH_IMAGE_URL]	URLs d'images Unsplash (à remplacer).	Hero, Service Cards, Backgrounds
Génère maintenant le code source complet en commençant par les fichiers de configuration (package.json, tailwind.config.js) puis en détaillant la structure des dossiers et le code des composants clés (Header.tsx, app/page.tsx, MultiStepForm.tsx).