"""
Phase 3: Section Agent - Sections réutilisables de la homepage
Génère TOUTES les sections modernes avec les composants UI de Phase 2
"""
from typing import Dict, Any


class SectionAgent:
    """Agent Phase 3: Sections homepage avec design moderne"""

    @staticmethod
    def get_prompt(business: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """
        Génère le prompt de création des sections homepage

        Ce prompt est ENRICHI avec :
        - Toutes les sections de la homepage (Hero, Stats, Services, Process, etc.)
        - Utilisation des composants UI de Phase 2
        - Animations Framer Motion avancées
        - Responsive design parfait
        - SEO optimisé avec balises sémantiques
        - Micro-interactions pour engagement utilisateur
        """
        services_list = business.get('services', '').split(',')
        service_principal = services_list[0].strip() if services_list else 'nos services'

        return f"""Tu es l'agent Section spécialisé dans la création de sections homepage modernes, engageantes et performantes.

📋 CONTEXTE:
Tu travailles sur le projet dans {site_dir}
Les Phases 1 (Setup) et 2 (Components) sont TERMINÉES.
Tous les composants UI sont disponibles dans {site_dir}/components/ui/

🏢 BUSINESS INFO:
- Entreprise: {business.get('name', '')}
- Ville: {business.get('city', '')}
- Services: {business.get('services', '')}
- Positionnement: {business.get('positioning', '')}
- Année création: {business.get('year', '')}
- Téléphone: {business.get('phone', '')}
- Email: {business.get('email', '')}
- Adresse: {business.get('street', '')}, {business.get('postal_code', '')} {business.get('city', '')}
- Horaires: {business.get('hours', 'Lundi-Vendredi 8h-18h')}

🎯 TA MISSION:
Créer TOUTES les sections de la homepage dans {site_dir}/components/sections/ avec:
- Design moderne et professionnel
- Animations Framer Motion avancées
- Responsive parfait (mobile-first)
- SEO optimisé (balises sémantiques)
- Accessibilité WCAG AA
- Performance optimale

═══════════════════════════════════════════════════════════
🚀 SECTION 1: Hero.tsx (SECTION PRINCIPALE)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/sections/Hero.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ Phone, Mail, MapPin, Clock, ArrowRight, Star }} from 'lucide-react';
import {{ Button }} from '@/components/ui';

export function Hero() {{
  const fadeInUp = {{
    initial: {{ opacity: 0, y: 30 }},
    animate: {{ opacity: 1, y: 0 }},
    transition: {{ duration: 0.8, ease: 'easeOut' }}
  }};

  const staggerContainer = {{
    animate: {{
      transition: {{
        staggerChildren: 0.15
      }}
    }}
  }};

  return (
    <section className="relative min-h-screen flex items-center bg-gradient-hero overflow-hidden">
      {{/* Background Pattern */}}
      <div className="absolute inset-0 bg-grid-pattern opacity-5" />

      {{/* Animated Background Blobs */}}
      <motion.div
        className="absolute top-20 -left-40 w-96 h-96 bg-accent/20 rounded-full blur-3xl"
        animate={{{{
          scale: [1, 1.2, 1],
          x: [0, 50, 0],
          y: [0, 30, 0]
        }}}}
        transition={{{{
          duration: 20,
          repeat: Infinity,
          ease: 'easeInOut'
        }}}}
      />
      <motion.div
        className="absolute bottom-20 -right-40 w-96 h-96 bg-primary/20 rounded-full blur-3xl"
        animate={{{{
          scale: [1, 1.3, 1],
          x: [0, -50, 0],
          y: [0, -30, 0]
        }}}}
        transition={{{{
          duration: 25,
          repeat: Infinity,
          ease: 'easeInOut'
        }}}}
      />

      <div className="section-container relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {{/* Left Column - Content */}}
          <motion.div
            variants={{staggerContainer}}
            initial="initial"
            animate="animate"
            className="text-white"
          >
            {{/* Trust Badge */}}
            <motion.div variants={{fadeInUp}} className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full mb-6 border border-white/20">
              <Star className="h-5 w-5 text-accent fill-accent" />
              <span className="text-sm font-medium">Expert depuis {business.get('year', '2020')}</span>
            </motion.div>

            {{/* Headline */}}
            <motion.h1 variants={{fadeInUp}} className="text-hero font-black mb-6 leading-tight">
              {business.get('positioning', 'Votre Expert Local')}
            </motion.h1>

            {{/* Subheadline */}}
            <motion.p variants={{fadeInUp}} className="text-h3 mb-8 text-white/90 leading-relaxed">
              {service_principal} professionnel à {business.get('city', '')} et alentours.
              Intervention rapide, devis gratuit, satisfaction garantie.
            </motion.p>

            {{/* CTA Buttons */}}
            <motion.div variants={{fadeInUp}} className="flex flex-wrap gap-4 mb-12">
              <Button
                variant="accent"
                size="xl"
                rightIcon={{<ArrowRight className="h-6 w-6" />}}
                onClick={{() => document.getElementById('contact-form')?.scrollIntoView({{ behavior: 'smooth' }})}}
              >
                Devis Gratuit
              </Button>

              <Button
                variant="outline"
                size="xl"
                leftIcon={{<Phone className="h-6 w-6" />}}
                className="bg-white/10 backdrop-blur-sm border-white/30 text-white hover:bg-white hover:text-primary"
                onClick={{() => window.location.href = 'tel:{business.get('phone', '')}'}}
              >
                {business.get('phone', '')}
              </Button>
            </motion.div>

            {{/* Quick Info Cards */}}
            <motion.div variants={{fadeInUp}} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex items-center gap-3 p-4 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
                <Clock className="h-8 w-8 text-accent flex-shrink-0" />
                <div>
                  <p className="text-sm text-white/70">Disponibilité</p>
                  <p className="font-semibold">{business.get('hours', 'Lun-Ven 8h-18h')}</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-4 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
                <MapPin className="h-8 w-8 text-accent flex-shrink-0" />
                <div>
                  <p className="text-sm text-white/70">Zone d'intervention</p>
                  <p className="font-semibold">{business.get('city', '')} + 30km</p>
                </div>
              </div>
            </motion.div>
          </motion.div>

          {{/* Right Column - Image/Visual */}}
          <motion.div
            initial={{{{ opacity: 0, scale: 0.8 }}}}
            animate={{{{ opacity: 1, scale: 1 }}}}
            transition={{{{ duration: 1, delay: 0.3 }}}}
            className="relative hidden lg:block"
          >
            <div className="relative aspect-square max-w-lg mx-auto">
              {{/* Decorative Elements */}}
              <div className="absolute inset-0 bg-gradient-to-br from-accent to-accent-700 rounded-4xl rotate-6 opacity-20 blur-2xl" />

              {{/* Main Image Container */}}
              <div className="relative bg-white/10 backdrop-blur-md rounded-4xl p-8 border border-white/20">
                <div className="bg-white rounded-3xl aspect-square flex items-center justify-center">
                  <p className="text-6xl font-black text-gradient">{business.get('name', '').split(' ')[0]}</p>
                </div>
              </div>

              {{/* Floating Stats */}}
              <motion.div
                animate={{{{ y: [-10, 10, -10] }}}}
                transition={{{{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}}}
                className="absolute -top-6 -right-6 bg-white p-6 rounded-2xl shadow-2xl"
              >
                <p className="text-3xl font-black text-primary">100%</p>
                <p className="text-sm text-gray-600">Satisfaits</p>
              </motion.div>

              <motion.div
                animate={{{{ y: [10, -10, 10] }}}}
                transition={{{{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}}}
                className="absolute -bottom-6 -left-6 bg-accent text-white p-6 rounded-2xl shadow-2xl"
              >
                <p className="text-3xl font-black">24/7</p>
                <p className="text-sm">Dispo</p>
              </motion.div>
            </div>
          </motion.div>
        </div>

        {{/* Scroll Indicator */}}
        <motion.div
          initial={{{{ opacity: 0 }}}}
          animate={{{{ opacity: 1 }}}}
          transition={{{{ delay: 1.5 }}}}
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
        >
          <motion.div
            animate={{{{ y: [0, 10, 0] }}}}
            transition={{{{ duration: 2, repeat: Infinity }}}}
            className="w-6 h-10 border-2 border-white/50 rounded-full flex items-start justify-center p-2"
          >
            <motion.div className="w-1.5 h-1.5 bg-white rounded-full" />
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}}
```

═══════════════════════════════════════════════════════════
📊 SECTION 2: Stats.tsx (CHIFFRES CLÉS)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/sections/Stats.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ useInView }} from 'framer-motion';
import {{ useRef, useState, useEffect }} from 'react';

interface StatItem {{
  value: number;
  suffix: string;
  label: string;
  prefix?: string;
}}

export function Stats() {{
  const stats: StatItem[] = [
    {{ value: 500, suffix: '+', label: 'Clients Satisfaits' }},
    {{ value: {2025 - int(business.get('year', 2020))}, suffix: ' ans', label: 'D\\'Expérience' }},
    {{ value: 100, suffix: '%', label: 'Garantie Qualité' }},
    {{ value: 24, suffix: 'h', label: 'Intervention Rapide' }},
  ];

  return (
    <section className="py-16 bg-gradient-to-br from-gray-50 to-white">
      <div className="section-container">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
          {{stats.map((stat, index) => (
            <StatCard key={{index}} stat={{stat}} index={{index}} />
          ))}}
        </div>
      </div>
    </section>
  );
}}

function StatCard({{ stat, index }}: {{ stat: StatItem; index: number }}) {{
  const ref = useRef(null);
  const isInView = useInView(ref, {{ once: true }});
  const [count, setCount] = useState(0);

  useEffect(() => {{
    if (isInView) {{
      let start = 0;
      const end = stat.value;
      const duration = 2000;
      const increment = end / (duration / 16);

      const timer = setInterval(() => {{
        start += increment;
        if (start >= end) {{
          setCount(end);
          clearInterval(timer);
        }} else {{
          setCount(Math.floor(start));
        }}
      }}, 16);

      return () => clearInterval(timer);
    }}
  }}, [isInView, stat.value]);

  return (
    <motion.div
      ref={{ref}}
      initial={{{{ opacity: 0, y: 30 }}}}
      animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
      transition={{{{ duration: 0.6, delay: index * 0.1 }}}}
      className="text-center"
    >
      <div className="relative inline-block">
        <motion.p
          className="text-5xl lg:text-6xl font-black text-gradient mb-2"
          animate={{{{ scale: isInView ? [1, 1.1, 1] : 1 }}}}
          transition={{{{ duration: 0.5, delay: index * 0.1 + 0.3 }}}}
        >
          {{stat.prefix}}{{count}}{{stat.suffix}}
        </motion.p>

        {{/* Decorative element */}}
        <motion.div
          className="absolute -inset-4 bg-accent/5 rounded-2xl -z-10"
          initial={{{{ scale: 0 }}}}
          animate={{{{ scale: isInView ? 1 : 0 }}}}
          transition={{{{ duration: 0.5, delay: index * 0.1 + 0.2 }}}}
        />
      </div>

      <p className="text-gray-600 font-medium mt-2">{{stat.label}}</p>
    </motion.div>
  );
}}
```

═══════════════════════════════════════════════════════════
🛠️ SECTION 3: Services.tsx (GRILLE DE SERVICES)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/sections/Services.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ useInView }} from 'framer-motion';
import {{ useRef }} from 'react';
import {{ Card, Button }} from '@/components/ui';
import {{ ArrowRight, Check }} from 'lucide-react';

export function Services() {{
  const services = `{business.get('services', '')}`.split(',').map(s => s.trim());

  const serviceDetails = services.map((service, index) => ({{
    title: service,
    description: `Service professionnel de ${{service.toLowerCase()}} avec garantie satisfaction et intervention rapide sur {business.get('city', '')} et alentours.`,
    features: [
      'Devis gratuit détaillé',
      'Intervention sous 24h',
      'Garantie qualité',
      'Tarifs transparents'
    ],
    icon: '🔧' // Vous pouvez personnaliser par service
  }}));

  const ref = useRef(null);
  const isInView = useInView(ref, {{ once: true, margin: '-100px' }});

  return (
    <section id="services" className="section-container" ref={{ref}}>
      {{/* Header */}}
      <motion.div
        initial={{{{ opacity: 0, y: 30 }}}}
        animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
        transition={{{{ duration: 0.8 }}}}
        className="text-center max-w-3xl mx-auto mb-16"
      >
        <p className="text-accent font-bold text-lg mb-4">Nos Services</p>
        <h2 className="text-h1 font-black mb-6">
          Solutions Professionnelles à {business.get('city', '')}
        </h2>
        <p className="text-body-large text-gray-600">
          {business.get('positioning', '')}. Expertise reconnue et service de qualité depuis {business.get('year', '')}.
        </p>
      </motion.div>

      {{/* Services Grid */}}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {{serviceDetails.map((service, index) => (
          <motion.div
            key={{index}}
            initial={{{{ opacity: 0, y: 30 }}}}
            animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
            transition={{{{ duration: 0.6, delay: index * 0.1 }}}}
          >
            <Card variant="elevated" padding="lg" hover className="h-full flex flex-col">
              {{/* Icon */}}
              <div className="w-16 h-16 bg-gradient-to-br from-primary to-accent rounded-2xl flex items-center justify-center text-3xl mb-6 shadow-glow">
                {{service.icon}}
              </div>

              {{/* Title */}}
              <h3 className="text-h3 font-bold mb-4 text-gray-900">
                {{service.title}}
              </h3>

              {{/* Description */}}
              <p className="text-gray-600 mb-6 flex-grow">
                {{service.description}}
              </p>

              {{/* Features */}}
              <ul className="space-y-3 mb-6">
                {{service.features.map((feature, idx) => (
                  <li key={{idx}} className="flex items-start gap-2">
                    <Check className="h-5 w-5 text-accent flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-gray-700">{{feature}}</span>
                  </li>
                ))}}
              </ul>

              {{/* CTA */}}
              <Button
                variant="outline"
                fullWidth
                rightIcon={{<ArrowRight className="h-5 w-5" />}}
                onClick={{() => document.getElementById('contact-form')?.scrollIntoView({{ behavior: 'smooth' }})}}
              >
                Demander un devis
              </Button>
            </Card>
          </motion.div>
        ))}}
      </div>

      {{/* Bottom CTA */}}
      <motion.div
        initial={{{{ opacity: 0, y: 30 }}}}
        animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
        transition={{{{ duration: 0.8, delay: 0.5 }}}}
        className="text-center mt-16"
      >
        <p className="text-gray-600 mb-6">Vous ne trouvez pas le service recherché ?</p>
        <Button
          variant="primary"
          size="lg"
          onClick={{() => window.location.href = 'tel:{business.get('phone', '')}'}}
        >
          Contactez-nous au {business.get('phone', '')}
        </Button>
      </motion.div>
    </section>
  );
}}
```

═══════════════════════════════════════════════════════════
⭐ SECTION 4: Testimonials.tsx (TÉMOIGNAGES)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/sections/Testimonials.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ useInView }} from 'framer-motion';
import {{ useRef }} from 'react';
import {{ Card }} from '@/components/ui';
import {{ Star, Quote }} from 'lucide-react';

export function Testimonials() {{
  const testimonials = [
    {{
      name: 'Marie D.',
      location: business.get('city', ''),
      rating: 5,
      text: `Service impeccable ! L'équipe de {business.get('name', '')} a résolu mon problème rapidement et professionnellement. Je recommande vivement.`,
      service: business.get('services', '').split(',')[0].trim()
    }},
    {{
      name: 'Jean-Paul L.',
      location: business.get('city', ''),
      rating: 5,
      text: 'Très satisfait de la prestation. Travail soigné, devis respecté et excellent contact. Je referai appel à eux sans hésiter.',
      service: business.get('services', '').split(',')[1]?.trim() || 'Service'
    }},
    {{
      name: 'Sophie M.',
      location: business.get('city', ''),
      rating: 5,
      text: `Intervention rapide et efficace. Le technicien était à l'heure, professionnel et a pris le temps de bien expliquer. Excellent rapport qualité-prix.`,
      service: business.get('services', '').split(',')[0].trim()
    }}
  ];

  const ref = useRef(null);
  const isInView = useInView(ref, {{ once: true, margin: '-100px' }});

  return (
    <section className="py-24 bg-gradient-to-br from-gray-50 to-white" ref={{ref}}>
      <div className="section-container">
        {{/* Header */}}
        <motion.div
          initial={{{{ opacity: 0, y: 30 }}}}
          animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
          transition={{{{ duration: 0.8 }}}}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <p className="text-accent font-bold text-lg mb-4">Témoignages</p>
          <h2 className="text-h1 font-black mb-6">
            Ce Que Disent Nos Clients
          </h2>
          <p className="text-body-large text-gray-600">
            La satisfaction de nos clients est notre priorité. Découvrez leurs avis.
          </p>
        </motion.div>

        {{/* Testimonials Grid */}}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {{testimonials.map((testimonial, index) => (
            <motion.div
              key={{index}}
              initial={{{{ opacity: 0, y: 30 }}}}
              animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
              transition={{{{ duration: 0.6, delay: index * 0.15 }}}}
            >
              <Card variant="elevated" padding="lg" hover className="h-full relative">
                {{/* Quote Icon */}}
                <div className="absolute top-6 right-6 text-accent/10">
                  <Quote className="h-16 w-16" />
                </div>

                {{/* Rating */}}
                <div className="flex gap-1 mb-4">
                  {{[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={{i}} className="h-5 w-5 text-accent fill-accent" />
                  ))}}
                </div>

                {{/* Testimonial Text */}}
                <p className="text-gray-700 mb-6 leading-relaxed relative z-10">
                  "{{testimonial.text}}"
                </p>

                {{/* Service Badge */}}
                <div className="inline-block px-3 py-1 bg-primary/10 text-primary text-sm font-medium rounded-full mb-4">
                  {{testimonial.service}}
                </div>

                {{/* Author */}}
                <div className="pt-4 border-t border-gray-100">
                  <p className="font-bold text-gray-900">{{testimonial.name}}</p>
                  <p className="text-sm text-gray-600">{{testimonial.location}}</p>
                </div>
              </Card>
            </motion.div>
          ))}}
        </div>

        {{/* Trust Indicators */}}
        <motion.div
          initial={{{{ opacity: 0, y: 30 }}}}
          animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
          transition={{{{ duration: 0.8, delay: 0.6 }}}}
          className="mt-16 text-center"
        >
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-white rounded-full shadow-lg">
            <Star className="h-6 w-6 text-accent fill-accent" />
            <span className="font-bold text-2xl text-gray-900">4.9/5</span>
            <span className="text-gray-600">· Basé sur 500+ avis clients</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}}
```

═══════════════════════════════════════════════════════════
❓ SECTION 5: FAQ.tsx (QUESTIONS FRÉQUENTES)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/sections/FAQ.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ useInView }} from 'framer-motion';
import {{ useRef }} from 'react';
import {{ Accordion, AccordionItem }} from '@/components/ui';

export function FAQ() {{
  const faqItems: AccordionItem[] = [
    {{
      id: 'faq-1',
      question: 'Quels sont vos tarifs ?',
      answer: `Nos tarifs varient selon la nature de l'intervention. Nous proposons systématiquement un devis gratuit et détaillé avant toute intervention. Contactez-nous au {business.get('phone', '')} pour obtenir une estimation précise adaptée à vos besoins.`
    }},
    {{
      id: 'faq-2',
      question: 'Intervenez-vous en urgence ?',
      answer: `Oui, nous proposons un service d'intervention rapide sur {business.get('city', '')} et alentours. Selon la disponibilité, nous pouvons intervenir sous 24h pour les urgences. Appelez-nous pour connaître nos disponibilités immédiates.`
    }},
    {{
      id: 'faq-3',
      question: 'Quelle est votre zone d\\'intervention ?',
      answer: `Nous intervenons principalement sur {business.get('city', '')} et dans un rayon de 30 km. Pour des interventions en dehors de cette zone, contactez-nous pour étudier votre demande.`
    }},
    {{
      id: 'faq-4',
      question: 'Proposez-vous une garantie ?',
      answer: `Oui, tous nos travaux sont garantis. La durée de garantie varie selon la nature de l'intervention. Nous vous fournissons systématiquement un certificat de garantie détaillant les conditions et la durée applicable à votre intervention.`
    }},
    {{
      id: 'faq-5',
      question: 'Comment obtenir un devis ?',
      answer: `Très simple ! Vous pouvez nous contacter par téléphone au {business.get('phone', '')}, par email à {business.get('email', '')}, ou remplir notre formulaire de contact en ligne. Nous vous répondons rapidement avec un devis gratuit et sans engagement.`
    }},
    {{
      id: 'faq-6',
      question: 'Acceptez-vous les paiements par carte ?',
      answer: `Oui, nous acceptons plusieurs modes de paiement pour votre confort : espèces, chèque, virement bancaire et carte bancaire. Le paiement s'effectue après réalisation des travaux et votre validation complète.`
    }}
  ];

  const ref = useRef(null);
  const isInView = useInView(ref, {{ once: true, margin: '-100px' }});

  return (
    <section id="faq" className="section-container" ref={{ref}}>
      {{/* Header */}}
      <motion.div
        initial={{{{ opacity: 0, y: 30 }}}}
        animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
        transition={{{{ duration: 0.8 }}}}
        className="text-center max-w-3xl mx-auto mb-16"
      >
        <p className="text-accent font-bold text-lg mb-4">Questions Fréquentes</p>
        <h2 className="text-h1 font-black mb-6">
          Vous Avez Des Questions ?
        </h2>
        <p className="text-body-large text-gray-600">
          Retrouvez les réponses aux questions les plus fréquentes. Pour toute autre question, n'hésitez pas à nous contacter.
        </p>
      </motion.div>

      {{/* FAQ Accordion */}}
      <motion.div
        initial={{{{ opacity: 0, y: 30 }}}}
        animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
        transition={{{{ duration: 0.8, delay: 0.2 }}}}
        className="max-w-4xl mx-auto"
      >
        <Accordion items={{faqItems}} />
      </motion.div>

      {{/* Bottom CTA */}}
      <motion.div
        initial={{{{ opacity: 0, y: 30 }}}}
        animate={{{{ opacity: isInView ? 1 : 0, y: isInView ? 0 : 30 }}}}
        transition={{{{ duration: 0.8, delay: 0.4 }}}}
        className="text-center mt-16 p-8 bg-gradient-to-br from-primary/5 to-accent/5 rounded-3xl"
      >
        <h3 className="text-h3 font-bold mb-4">Vous ne trouvez pas votre réponse ?</h3>
        <p className="text-gray-600 mb-6">Notre équipe est à votre disposition pour répondre à toutes vos questions</p>
        <div className="flex flex-wrap gap-4 justify-center">
          <a
            href="tel:{business.get('phone', '')}"
            className="btn-primary"
          >
            Appelez-nous
          </a>
          <a
            href="mailto:{business.get('email', '')}"
            className="btn-accent"
          >
            Envoyez un email
          </a>
        </div>
      </motion.div>
    </section>
  );
}}
```

═══════════════════════════════════════════════════════════
📞 SECTION 6: FinalCTA.tsx (APPEL À L'ACTION FINAL)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/sections/FinalCTA.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ Phone, Mail, Clock, MapPin, ArrowRight }} from 'lucide-react';
import {{ Button }} from '@/components/ui';

export function FinalCTA() {{
  return (
    <section className="relative py-24 bg-gradient-to-br from-primary via-primary-700 to-primary-900 overflow-hidden">
      {{/* Background Pattern */}}
      <div className="absolute inset-0 bg-grid-pattern opacity-5" />

      {{/* Animated Blobs */}}
      <motion.div
        className="absolute top-0 left-0 w-96 h-96 bg-accent/20 rounded-full blur-3xl"
        animate={{{{
          scale: [1, 1.2, 1],
          x: [0, 100, 0],
        }}}}
        transition={{{{ duration: 20, repeat: Infinity }}}}
      />

      <div className="section-container relative z-10">
        <div className="max-w-4xl mx-auto text-center text-white">
          {{/* Main CTA */}}
          <motion.div
            initial={{{{ opacity: 0, y: 30 }}}}
            whileInView={{{{ opacity: 1, y: 0 }}}}
            viewport={{{{ once: true }}}}
            transition={{{{ duration: 0.8 }}}}
          >
            <h2 className="text-h1 font-black mb-6">
              Prêt à Démarrer Votre Projet ?
            </h2>
            <p className="text-h3 mb-12 text-white/90">
              Obtenez votre devis gratuit en moins de 24h. Sans engagement.
            </p>

            <div className="flex flex-wrap gap-4 justify-center mb-16">
              <Button
                variant="accent"
                size="xl"
                rightIcon={{<ArrowRight className="h-6 w-6" />}}
                onClick={{() => document.getElementById('contact-form')?.scrollIntoView({{ behavior: 'smooth' }})}}
              >
                Devis Gratuit
              </Button>

              <Button
                variant="outline"
                size="xl"
                leftIcon={{<Phone className="h-6 w-6" />}}
                className="bg-white/10 backdrop-blur-sm border-white/30 text-white hover:bg-white hover:text-primary"
                onClick={{() => window.location.href = 'tel:{business.get('phone', '')}'}}
              >
                {business.get('phone', '')}
              </Button>
            </div>
          </motion.div>

          {{/* Contact Info Cards */}}
          <motion.div
            initial={{{{ opacity: 0, y: 30 }}}}
            whileInView={{{{ opacity: 1, y: 0 }}}}
            viewport={{{{ once: true }}}}
            transition={{{{ duration: 0.8, delay: 0.2 }}}}
            className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
          >
            <div className="p-6 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
              <Phone className="h-8 w-8 text-accent mb-3 mx-auto" />
              <p className="text-sm text-white/70 mb-1">Téléphone</p>
              <p className="font-semibold">{business.get('phone', '')}</p>
            </div>

            <div className="p-6 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
              <Mail className="h-8 w-8 text-accent mb-3 mx-auto" />
              <p className="text-sm text-white/70 mb-1">Email</p>
              <p className="font-semibold break-all">{business.get('email', '')}</p>
            </div>

            <div className="p-6 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
              <Clock className="h-8 w-8 text-accent mb-3 mx-auto" />
              <p className="text-sm text-white/70 mb-1">Horaires</p>
              <p className="font-semibold">{business.get('hours', 'Lun-Ven 8h-18h')}</p>
            </div>

            <div className="p-6 bg-white/10 backdrop-blur-sm rounded-2xl border border-white/20">
              <MapPin className="h-8 w-8 text-accent mb-3 mx-auto" />
              <p className="text-sm text-white/70 mb-1">Localisation</p>
              <p className="font-semibold">{business.get('city', '')}</p>
            </div>
          </motion.div>

          {{/* Trust Badge */}}
          <motion.div
            initial={{{{ opacity: 0 }}}}
            whileInView={{{{ opacity: 1 }}}}
            viewport={{{{ once: true }}}}
            transition={{{{ duration: 0.8, delay: 0.4 }}}}
            className="mt-12 text-white/70 text-sm"
          >
            <p>✓ Devis gratuit · ✓ Sans engagement · ✓ Réponse sous 24h</p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}}
```

═══════════════════════════════════════════════════════════
📦 EXPORT CENTRALISÉ
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/sections/index.ts:

```typescript
export {{ Hero }} from './Hero';
export {{ Stats }} from './Stats';
export {{ Services }} from './Services';
export {{ Testimonials }} from './Testimonials';
export {{ FAQ }} from './FAQ';
export {{ FinalCTA }} from './FinalCTA';
```

═══════════════════════════════════════════════════════════
✅ CRITÈRES DE SUCCÈS
═══════════════════════════════════════════════════════════

Vérifie que :
✓ Toutes les 6 sections sont créées
✓ Chaque section utilise les composants UI de Phase 2
✓ Framer Motion animations intégrées (fadeIn, scroll triggers)
✓ Responsive design parfait (mobile-first)
✓ Accessibilité complète (balises sémantiques, ARIA)
✓ SEO optimisé (structure HTML sémantique)
✓ Toutes les infos business injectées dynamiquement
✓ components/sections/index.ts créé pour exports
✓ Aucune erreur TypeScript

Une fois terminé, réponds avec:
- Liste des 6 sections créées
- Confirmation que toutes utilisent les composants Phase 2
- Prêt pour Phase 4 (Pages)"""
