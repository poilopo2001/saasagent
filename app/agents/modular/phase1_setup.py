"""
Phase 1: Setup Agent - Structure du projet + Configuration complète
Crée la base solide avec toute la configuration Next.js/Tailwind/TypeScript
"""
from typing import Dict, Any


class SetupAgent:
    """Agent Phase 1: Setup complet du projet Next.js"""

    @staticmethod
    def get_prompt(business: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """
        Génère le prompt de setup initial avec TOUTE la configuration

        Ce prompt est ENRICHI avec :
        - Configuration Tailwind complète avec toutes les teintes de couleurs
        - Next.config.mjs optimisé pour performance et SEO
        - TypeScript strict mode avec types précis
        - Package.json avec TOUTES les dépendances nécessaires
        - Structure de dossiers complète et optimisée
        - Configuration ESLint et Prettier pour qualité code
        """
        return f"""Tu es l'agent Setup spécialisé dans la création de la structure et configuration parfaite d'un projet Next.js 14+ moderne.

📋 CONTEXTE BUSINESS:
- Entreprise: {business.get('name', '')}
- Ville: {business.get('city', '')}
- Secteur: {business.get('services', '').split(',')[0] if business.get('services') else 'services'}
- Couleur Primary: {business.get('primary_color', '#1a5490')}
- Couleur Accent: {business.get('secondary_color', '#ff8c42')}

📁 RÉPERTOIRE: {site_dir}

🎯 TA MISSION:
Créer la structure de base COMPLÈTE et OPTIMALE pour un site Next.js 14+ avec App Router, TypeScript strict, et Tailwind CSS customisé.

═══════════════════════════════════════════════════════════
📦 ÉTAPE 1: CRÉER package.json COMPLET
═══════════════════════════════════════════════════════════

Crée {site_dir}/package.json avec TOUTES les dépendances nécessaires:

{{
  "name": "{site_slug}",
  "version": "1.0.0",
  "private": true,
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }},
  "dependencies": {{
    "next": "^14.2.18",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "framer-motion": "^12.0.0",
    "lucide-react": "^0.468.0",
    "react-hook-form": "^7.54.2",
    "zod": "^3.24.1",
    "@hookform/resolvers": "^3.9.1",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.6.0"
  }},
  "devDependencies": {{
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "typescript": "^5",
    "tailwindcss": "^3.4.17",
    "postcss": "^8",
    "autoprefixer": "^10.4.20",
    "eslint": "^8",
    "eslint-config-next": "14.2.18"
  }}
}}

═══════════════════════════════════════════════════════════
🎨 ÉTAPE 2: CRÉER tailwind.config.js ULTRA-DÉTAILLÉ
═══════════════════════════════════════════════════════════

Crée {site_dir}/tailwind.config.js avec TOUTES les teintes de couleurs personnalisées:

/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    './pages/**/*.{{js,ts,jsx,tsx,mdx}}',
    './components/**/*.{{js,ts,jsx,tsx,mdx}}',
    './app/**/*.{{js,ts,jsx,tsx,mdx}}',
  ],
  theme: {{
    extend: {{
      colors: {{
        primary: {{
          DEFAULT: '{business.get('primary_color', '#1a5490')}',
          50: '#e6f0f9',
          100: '#cce1f3',
          200: '#99c3e7',
          300: '#66a5db',
          400: '#3387cf',
          500: '#1a5490',  // Base color
          600: '#154373',
          700: '#103256',
          800: '#0b2139',
          900: '#05111c',
        }},
        accent: {{
          DEFAULT: '{business.get('secondary_color', '#ff8c42')}',
          50: '#fff4ed',
          100: '#ffe9db',
          200: '#ffd3b7',
          300: '#ffbd93',
          400: '#ffa76f',
          500: '#ff8c42',  // Base color
          600: '#ff7519',
          700: '#e65a00',
          800: '#b34600',
          900: '#803300',
        }},
      }},
      fontFamily: {{
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }},
      fontSize: {{
        'hero': ['clamp(2.5rem, 8vw, 5rem)', {{ lineHeight: '1', letterSpacing: '-0.02em' }}],
        'h1': ['clamp(2rem, 5vw, 3rem)', {{ lineHeight: '1.2', letterSpacing: '-0.01em' }}],
        'h2': ['clamp(1.75rem, 4vw, 2.5rem)', {{ lineHeight: '1.3' }}],
        'h3': ['clamp(1.5rem, 3vw, 2rem)', {{ lineHeight: '1.4' }}],
        'body-large': ['1.125rem', {{ lineHeight: '1.75' }}],
        'body': ['1rem', {{ lineHeight: '1.75' }}],
      }},
      spacing: {{
        '128': '32rem',
        '144': '36rem',
      }},
      borderRadius: {{
        '4xl': '2rem',
      }},
      boxShadow: {{
        'glow': '0 0 20px rgba(255, 140, 66, 0.4)',
        'glow-lg': '0 0 30px rgba(255, 140, 66, 0.5)',
      }},
      animation: {{
        'fadeInUp': 'fadeInUp 0.8s ease-out',
        'float': 'float 3s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
      }},
      keyframes: {{
        fadeInUp: {{
          '0%': {{ opacity: '0', transform: 'translateY(30px)' }},
          '100%': {{ opacity: '1', transform: 'translateY(0)' }},
        }},
        float: {{
          '0%, 100%': {{ transform: 'translateY(0)' }},
          '50%': {{ transform: 'translateY(-10px)' }},
        }},
        'pulse-glow': {{
          '0%, 100%': {{ boxShadow: '0 0 20px rgba(255, 140, 66, 0.4)' }},
          '50%': {{ boxShadow: '0 0 30px rgba(255, 140, 66, 0.7)' }},
        }},
      }},
    }},
  }},
  plugins: [],
}}

═══════════════════════════════════════════════════════════
⚙️ ÉTAPE 3: CRÉER next.config.mjs OPTIMISÉ
═══════════════════════════════════════════════════════════

Crée {site_dir}/next.config.mjs avec configuration performance et SEO:

/** @type {{import('next').NextConfig}} */
const nextConfig = {{
  images: {{
    remotePatterns: [
      {{
        protocol: 'https',
        hostname: 'images.unsplash.com',
      }},
      {{
        protocol: 'https',
        hostname: 'source.unsplash.com',
      }},
    ],
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  }},
  experimental: {{
    optimizeCss: true,
  }},
  compress: true,
  poweredByHeader: false,
  reactStrictMode: true,
}};

export default nextConfig;

═══════════════════════════════════════════════════════════
📝 ÉTAPE 4: CRÉER tsconfig.json STRICT
═══════════════════════════════════════════════════════════

Crée {site_dir}/tsconfig.json avec TypeScript strict mode:

{{
  "compilerOptions": {{
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {{
        "name": "next"
      }}
    ],
    "paths": {{
      "@/*": ["./*"]
    }}
  }},
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}}

═══════════════════════════════════════════════════════════
🏗️ ÉTAPE 5: CRÉER LA STRUCTURE DE DOSSIERS COMPLÈTE
═══════════════════════════════════════════════════════════

Crée TOUS les dossiers nécessaires:

{site_dir}/
├── app/
│   ├── (pages)/                    # Route group pour pages
│   │   ├── contact/
│   │   ├── nos-services/
│   │   ├── realisations/
│   │   ├── devis-gratuit/
│   │   ├── mentions-legales/
│   │   └── politique-confidentialite/
│   └── [slug-service]/            # Dynamic routes pour services
├── components/
│   ├── ui/                        # Composants de base
│   ├── layout/                    # Header, Footer, Navigation
│   ├── sections/                  # Sections réutilisables homepage
│   ├── forms/                     # Formulaires
│   └── utils/                     # Utilitaires (sliders, counters)
├── lib/
│   ├── utils/                     # Helper functions
│   └── hooks/                     # Custom React hooks
├── public/
│   └── images/
└── types/

═══════════════════════════════════════════════════════════
📄 ÉTAPE 6: CRÉER LES FICHIERS DE BASE
═══════════════════════════════════════════════════════════

Crée {site_dir}/postcss.config.mjs:

/** @type {{import('postcss-load-config').Config}} */
const config = {{
  plugins: {{
    tailwindcss: {{}},
    autoprefixer: {{}},
  }},
}};

export default config;

Crée {site_dir}/.eslintrc.json:

{{
  "extends": ["next/core-web-vitals", "next/typescript"]
}}

Crée {site_dir}/.gitignore:

# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local
.env

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts

# temp
/tmp
/.temp

═══════════════════════════════════════════════════════════
🎨 ÉTAPE 7: CRÉER app/globals.css AVEC STYLES DE BASE
═══════════════════════════════════════════════════════════

Crée {site_dir}/app/globals.css avec Tailwind + styles custom:

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {{
  :root {{
    --primary: {business.get('primary_color', '#1a5490')};
    --accent: {business.get('secondary_color', '#ff8c42')};
  }}

  * {{
    @apply border-gray-200;
  }}

  body {{
    @apply bg-white text-gray-900 antialiased;
  }}

  h1, h2, h3, h4, h5, h6 {{
    @apply font-bold tracking-tight;
  }}
}}

@layer components {{
  .btn-primary {{
    @apply bg-primary text-white px-6 py-3 rounded-lg font-semibold;
    @apply shadow-xl hover:bg-primary-600 hover:scale-105 active:scale-95;
    @apply transition-all duration-300 ease-in-out;
  }}

  .btn-accent {{
    @apply bg-accent text-white px-8 py-4 rounded-lg font-bold text-lg;
    @apply shadow-glow hover:shadow-glow-lg hover:bg-accent-600;
    @apply transition-all duration-300 ease-in-out;
  }}

  .card-modern {{
    @apply bg-white rounded-2xl p-8 border border-gray-100;
    @apply hover:shadow-2xl hover:border-accent transition-all duration-500;
  }}

  .section-container {{
    @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24;
  }}
}}

@layer utilities {{
  .text-gradient {{
    @apply bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent;
  }}

  .bg-gradient-hero {{
    @apply bg-gradient-to-br from-primary/90 to-primary-900/95;
  }}

  .bg-gradient-accent {{
    @apply bg-gradient-to-br from-accent/90 to-accent-700/95;
  }}
}}

═══════════════════════════════════════════════════════════
📦 ÉTAPE 8: INSTALLATION DES DÉPENDANCES
═══════════════════════════════════════════════════════════

Exécute dans {site_dir}:
```bash
npm install
```

IMPORTANT: Attend que npm install se termine COMPLÈTEMENT avant de continuer.

═══════════════════════════════════════════════════════════
✅ CRITÈRES DE SUCCÈS
═══════════════════════════════════════════════════════════

Vérifie que :
✓ Tous les fichiers de configuration sont créés
✓ package.json contient TOUTES les dépendances listées
✓ tailwind.config.js a les couleurs custom complètes (50-900)
✓ next.config.mjs a la config images pour Unsplash
✓ Structure de dossiers complète créée
✓ app/globals.css a les classes utilitaires custom
✓ npm install s'est exécuté sans erreurs
✓ node_modules existe et contient les packages

Une fois terminé, réponds avec un résumé:
- Nombre de fichiers créés
- Taille de node_modules
- Confirmation que tout est prêt pour Phase 2 (Components)"""
