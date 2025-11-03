"""
Phase 5: Content Agent - SEO, JSON-LD schemas, et polish final
Génère tous les éléments de contenu SEO et métadonnées structurées
"""
from typing import Dict, Any


class ContentAgent:
    """Agent Phase 5: Optimisation SEO et métadonnées"""

    @staticmethod
    def get_prompt(business: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """
        Génère le prompt de création du contenu SEO final

        Ce prompt est ENRICHI avec :
        - JSON-LD schemas (LocalBusiness, Organization, BreadcrumbList)
        - Meta tags Open Graph et Twitter
        - Sitemap.xml et robots.txt
        - Structured data pour Google Rich Results
        - Alt texts optimisés pour images
        - Aria labels pour accessibilité
        """
        services_list = business.get('services', '').split(',')

        return f"""Tu es l'agent Content spécialisé dans l'optimisation SEO et les métadonnées structurées pour un référencement optimal.

📋 CONTEXTE:
Tu travailles sur le projet dans {site_dir}
Les Phases 1, 2, 3 et 4 sont TERMINÉES:
- Phase 1: Setup + Configuration ✅
- Phase 2: Composants UI ✅
- Phase 3: Sections homepage ✅
- Phase 4: Pages + Layout ✅

Le site est fonctionnel. Il ne manque que le SEO et les métadonnées.

🏢 BUSINESS INFO:
- Entreprise: {business.get('name', '')}
- Ville: {business.get('city', '')}
- Pays: {business.get('country', 'Luxembourg')}
- Services: {business.get('services', '')}
- Téléphone: {business.get('phone', '')}
- Email: {business.get('email', '')}
- Adresse: {business.get('street', '')}, {business.get('postal_code', '')} {business.get('city', '')}
- URL: {business.get('domain_url', f'https://{site_slug}.com')}
- Année création: {business.get('year', '')}
- Horaires: {business.get('hours', 'Lundi-Vendredi 8h-18h')}

🎯 TA MISSION:
Créer TOUS les fichiers SEO et métadonnées dans {site_dir}/ avec:
- JSON-LD schemas pour Google Rich Results
- Sitemap.xml pour indexation
- Robots.txt optimisé
- Composant StructuredData réutilisable
- Meta tags sociaux (OG, Twitter)

═══════════════════════════════════════════════════════════
📊 FICHIER 1: components/seo/StructuredData.tsx (JSON-LD)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/seo/StructuredData.tsx:

```typescript
'use client';

export function StructuredData() {{
  const localBusinessSchema = {{
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    '@id': '{business.get('domain_url', f'https://{site_slug}.com')}',
    name: '{business.get('name', '')}',
    description: '{business.get('positioning', 'Service professionnel')} à {business.get('city', '')}. {business.get('services', '')}.',
    url: '{business.get('domain_url', f'https://{site_slug}.com')}',
    telephone: '{business.get('phone', '')}',
    email: '{business.get('email', '')}',
    priceRange: '$$',
    address: {{
      '@type': 'PostalAddress',
      streetAddress: '{business.get('street', '')}',
      addressLocality: '{business.get('city', '')}',
      postalCode: '{business.get('postal_code', '')}',
      addressCountry: '{business.get('country', 'LU')}',
    }},
    geo: {{
      '@type': 'GeoCoordinates',
      latitude: '49.6116',  // À adapter selon la ville
      longitude: '6.1319',
    }},
    openingHoursSpecification: [
      {{
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        opens: '08:00',
        closes: '18:00',
      }},
    ],
    sameAs: [
      'https://www.facebook.com/yourpage',
      'https://www.instagram.com/yourpage',
      'https://www.linkedin.com/company/yourpage',
    ],
    image: '{business.get('domain_url', f'https://{site_slug}.com')}/logo.png',
    aggregateRating: {{
      '@type': 'AggregateRating',
      ratingValue: '4.9',
      reviewCount: '500',
      bestRating: '5',
      worstRating: '1',
    }},
  }};

  const organizationSchema = {{
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: '{business.get('name', '')}',
    url: '{business.get('domain_url', f'https://{site_slug}.com')}',
    logo: '{business.get('domain_url', f'https://{site_slug}.com')}/logo.png',
    foundingDate: '{business.get('year', '')}',
    contactPoint: {{
      '@type': 'ContactPoint',
      telephone: '{business.get('phone', '')}',
      contactType: 'Customer Service',
      email: '{business.get('email', '')}',
      availableLanguage: ['French', 'German'],
      areaServed: '{business.get('country', 'LU')}',
    }},
  }};

  const breadcrumbSchema = {{
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {{
        '@type': 'ListItem',
        position: 1,
        name: 'Accueil',
        item: '{business.get('domain_url', f'https://{site_slug}.com')}',
      }},
      {{
        '@type': 'ListItem',
        position: 2,
        name: 'Services',
        item: '{business.get('domain_url', f'https://{site_slug}.com')}/#services',
      }},
      {{
        '@type': 'ListItem',
        position: 3,
        name: 'Contact',
        item: '{business.get('domain_url', f'https://{site_slug}.com')}/#contact',
      }},
    ],
  }};

  const serviceSchemas = [
{', '.join([f'''    {{
      '@context': 'https://schema.org',
      '@type': 'Service',
      name: '{service.strip()}',
      description: 'Service professionnel de {service.strip().lower()} à {business.get('city', '')} et alentours.',
      provider: {{
        '@type': 'LocalBusiness',
        name: '{business.get('name', '')}',
        telephone: '{business.get('phone', '')}',
      }},
      areaServed: {{
        '@type': 'City',
        name: '{business.get('city', '')}',
      }},
    }}''' for service in services_list[:3]])}
  ];

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{{{ __html: JSON.stringify(localBusinessSchema) }}}}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{{{ __html: JSON.stringify(organizationSchema) }}}}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{{{ __html: JSON.stringify(breadcrumbSchema) }}}}
      />
      {{serviceSchemas.map((schema, index) => (
        <script
          key={{index}}
          type="application/ld+json"
          dangerouslySetInnerHTML={{{{ __html: JSON.stringify(schema) }}}}
        />
      ))}}
    </>
  );
}}
```

═══════════════════════════════════════════════════════════
🗺️ FICHIER 2: public/sitemap.xml
═══════════════════════════════════════════════════════════

Crée {site_dir}/public/sitemap.xml:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{business.get('domain_url', f'https://{site_slug}.com')}</loc>
    <lastmod>{{{{new Date().toISOString().split('T')[0]}}}}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{business.get('domain_url', f'https://{site_slug}.com')}/mentions-legales</loc>
    <lastmod>{{{{new Date().toISOString().split('T')[0]}}}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>{business.get('domain_url', f'https://{site_slug}.com')}/politique-confidentialite</loc>
    <lastmod>{{{{new Date().toISOString().split('T')[0]}}}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
```

═══════════════════════════════════════════════════════════
🤖 FICHIER 3: public/robots.txt
═══════════════════════════════════════════════════════════

Crée {site_dir}/public/robots.txt:

```
# {business.get('name', '')} - Robots.txt

User-agent: *
Allow: /

# Sitemap
Sitemap: {business.get('domain_url', f'https://{site_slug}.com')}/sitemap.xml

# Block admin paths (if any in future)
Disallow: /api/
Disallow: /_next/
```

═══════════════════════════════════════════════════════════
🎨 FICHIER 4: public/manifest.json (PWA)
═══════════════════════════════════════════════════════════

Crée {site_dir}/public/manifest.json:

```json
{{
  "name": "{business.get('name', '')}",
  "short_name": "{business.get('name', '').split()[0]}",
  "description": "{business.get('positioning', '')} à {business.get('city', '')}",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "{business.get('primary_color', '#1a5490')}",
  "orientation": "portrait-primary",
  "icons": [
    {{
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    }},
    {{
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }}
  ]
}}
```

═══════════════════════════════════════════════════════════
📄 FICHIER 5: app/layout.tsx (MISE À JOUR AVEC SEO)
═══════════════════════════════════════════════════════════

Mets à jour {site_dir}/app/layout.tsx pour inclure StructuredData:

```typescript
import type {{ Metadata }} from 'next';
import {{ Inter }} from 'next/font/google';
import {{ StructuredData }} from '@/components/seo/StructuredData';
import './globals.css';

const inter = Inter({{ subsets: ['latin'] }});

export const metadata: Metadata = {{
  metadataBase: new URL('{business.get('domain_url', f'https://{site_slug}.com')}'),
  title: {{
    default: '{business.get('name', '')} - {business.get('positioning', '')} à {business.get('city', '')}',
    template: '%s | {business.get('name', '')}',
  }},
  description: `{business.get('services', '')} professionnel à {business.get('city', '')}. {business.get('positioning', '')}. Devis gratuit, intervention rapide, satisfaction garantie. Contactez-nous au {business.get('phone', '')}.`,
  keywords: [
    '{business.get('city', '')}',
{', '.join([f"    '{service.strip()}'" for service in services_list[:5]])},
    'devis gratuit',
    'intervention rapide',
    '{business.get('country', 'Luxembourg')}',
    'professionnel',
    'qualité garantie'
  ],
  authors: [{{ name: '{business.get('name', '')}', url: '{business.get('domain_url', f'https://{site_slug}.com')}' }}],
  creator: '{business.get('name', '')}',
  publisher: '{business.get('name', '')}',
  formatDetection: {{
    email: false,
    address: false,
    telephone: false,
  }},
  openGraph: {{
    type: 'website',
    locale: 'fr_FR',
    url: '{business.get('domain_url', f'https://{site_slug}.com')}',
    title: '{business.get('name', '')} - {business.get('positioning', '')}',
    description: `{business.get('services', '')} à {business.get('city', '')}. Devis gratuit et intervention rapide.`,
    siteName: '{business.get('name', '')}',
    images: [
      {{
        url: '{business.get('domain_url', f'https://{site_slug}.com')}/og-image.jpg',
        width: 1200,
        height: 630,
        alt: '{business.get('name', '')} - {business.get('positioning', '')}',
      }},
    ],
  }},
  twitter: {{
    card: 'summary_large_image',
    title: '{business.get('name', '')} - {business.get('positioning', '')}',
    description: `{business.get('services', '')} à {business.get('city', '')}`,
    images: ['{business.get('domain_url', f'https://{site_slug}.com')}/og-image.jpg'],
  }},
  robots: {{
    index: true,
    follow: true,
    googleBot: {{
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    }},
  }},
  icons: {{
    icon: [
      {{ url: '/favicon.ico' }},
      {{ url: '/icon-192.png', sizes: '192x192', type: 'image/png' }},
      {{ url: '/icon-512.png', sizes: '512x512', type: 'image/png' }},
    ],
    apple: [
      {{ url: '/apple-touch-icon.png' }},
    ],
  }},
  manifest: '/manifest.json',
  verification: {{
    google: 'your-google-verification-code-here',
  }},
  alternates: {{
    canonical: '{business.get('domain_url', f'https://{site_slug}.com')}',
  }},
}};

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode;
}}) {{
  return (
    <html lang="fr">
      <head>
        <StructuredData />
      </head>
      <body className={{inter.className}}>
        {{children}}
      </body>
    </html>
  );
}}
```

═══════════════════════════════════════════════════════════
📧 FICHIER 6: app/api/contact/route.ts (API CONTACT)
═══════════════════════════════════════════════════════════

Crée {site_dir}/app/api/contact/route.ts:

```typescript
import {{ NextResponse }} from 'next/server';

export async function POST(request: Request) {{
  try {{
    const body = await request.json();
    const {{ name, email, phone, service, message }} = body;

    // Validation basique
    if (!name || !email || !phone || !service || !message) {{
      return NextResponse.json(
        {{ error: 'Tous les champs sont requis' }},
        {{ status: 400 }}
      );
    }}

    // TODO: Envoyer l'email via service d'emailing (SendGrid, Resend, etc.)
    console.log('Nouvelle demande de contact:', {{
      name,
      email,
      phone,
      service,
      message,
      date: new Date().toISOString(),
    }});

    // Pour l'instant, on simule un succès
    // Dans une vraie app, remplacez par l'envoi d'email réel
    return NextResponse.json(
      {{
        success: true,
        message: 'Votre demande a été envoyée avec succès. Nous vous répondrons sous 24h.',
      }},
      {{ status: 200 }}
    );
  }} catch (error) {{
    console.error('Erreur lors du traitement du formulaire:', error);
    return NextResponse.json(
      {{ error: 'Une erreur est survenue. Veuillez réessayer.' }},
      {{ status: 500 }}
    );
  }}
}}
```

═══════════════════════════════════════════════════════════
🖼️ FICHIER 7: public/.gitkeep (DOSSIER IMAGES)
═══════════════════════════════════════════════════════════

Crée {site_dir}/public/.gitkeep pour créer le dossier public:

```
# Ce fichier permet de créer le dossier public même vide
# Les images seront ajoutées manuellement ou via un script
```

═══════════════════════════════════════════════════════════
📦 EXPORT SEO
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/seo/index.ts:

```typescript
export {{ StructuredData }} from './StructuredData';
```

═══════════════════════════════════════════════════════════
📝 FICHIER 8: README.md (DOCUMENTATION)
═══════════════════════════════════════════════════════════

Crée {site_dir}/README.md:

```markdown
# {business.get('name', '')}

Site web professionnel pour {business.get('name', '')} - {business.get('positioning', '')} à {business.get('city', '')}.

## 🚀 Technologies

- **Framework**: Next.js 14+ avec App Router
- **Styling**: Tailwind CSS avec design system personnalisé
- **Animations**: Framer Motion
- **Validation**: React Hook Form + Zod
- **TypeScript**: Strict mode activé
- **SEO**: JSON-LD schemas, sitemap, metadata optimisées

## 📦 Installation

```bash
npm install
```

## 🛠️ Développement

```bash
npm run dev
```

Ouvrir [http://localhost:3000](http://localhost:3000)

## 🏗️ Build Production

```bash
npm run build
npm start
```

## 📱 Fonctionnalités

- ✅ Design responsive (mobile-first)
- ✅ Formulaire de contact multi-étapes
- ✅ Navigation responsive avec menu mobile
- ✅ Animations smooth avec Framer Motion
- ✅ SEO optimisé (JSON-LD, Open Graph, Twitter Cards)
- ✅ Accessibilité WCAG AA
- ✅ Performance optimale (Core Web Vitals)
- ✅ PWA ready (manifest.json)

## 📞 Contact

**{business.get('name', '')}**
{business.get('street', '')}
{business.get('postal_code', '')} {business.get('city', '')}
📞 {business.get('phone', '')}
📧 {business.get('email', '')}

## 📄 License

© {business.get('year', '')} {business.get('name', '')}. Tous droits réservés.
```

═══════════════════════════════════════════════════════════
✅ CRITÈRES DE SUCCÈS
═══════════════════════════════════════════════════════════

Vérifie que :
✓ StructuredData component créé avec tous les schemas JSON-LD
✓ Sitemap.xml créé dans public/
✓ Robots.txt créé dans public/
✓ Manifest.json créé pour PWA
✓ Layout mis à jour avec metadata complètes
✓ API route /api/contact créée
✓ README.md documentation créé
✓ Tous les schemas incluent les bonnes infos business
✓ Open Graph et Twitter Cards configurés
✓ SEO metadata optimisées pour {business.get('city', '')}
✓ Aucune erreur TypeScript

Une fois terminé, réponds avec:
- Liste des fichiers SEO créés
- Confirmation des schemas JSON-LD (LocalBusiness, Organization, Service)
- Confirmation que le site est 100% prêt pour production
- Prêt pour build et déploiement !

🎉 FÉLICITATIONS ! Les 5 phases sont maintenant complètes."""
