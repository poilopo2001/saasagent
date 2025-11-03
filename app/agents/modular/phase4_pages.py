"""
Phase 4: Page Agent - Assemblage des pages complètes
Génère toutes les pages avec layout, navigation, formulaire de contact
"""
from typing import Dict, Any


class PageAgent:
    """Agent Phase 4: Pages complètes avec layout et navigation"""

    @staticmethod
    def get_prompt(business: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """
        Génère le prompt de création des pages complètes

        Ce prompt est ENRICHI avec :
        - Layout complet (Header, Footer, Navigation)
        - Page d'accueil assemblant toutes les sections
        - Formulaire de contact multi-étapes avec validation
        - Pages légales (mentions légales, politique de confidentialité)
        - Navigation responsive avec menu mobile
        - SEO metadata dans layout
        """
        return f"""Tu es l'agent Page spécialisé dans la création de pages complètes avec layout moderne et navigation optimale.

📋 CONTEXTE:
Tu travailles sur le projet dans {site_dir}
Les Phases 1, 2 et 3 sont TERMINÉES:
- Phase 1: Setup + Configuration ✅
- Phase 2: Composants UI ✅
- Phase 3: Sections homepage ✅

Tous les composants et sections sont disponibles et fonctionnels.

🏢 BUSINESS INFO:
- Entreprise: {business.get('name', '')}
- Ville: {business.get('city', '')}
- Services: {business.get('services', '')}
- Téléphone: {business.get('phone', '')}
- Email: {business.get('email', '')}
- Adresse: {business.get('street', '')}, {business.get('postal_code', '')} {business.get('city', '')}
- URL: {business.get('domain_url', f'https://{site_slug}.com')}

🎯 TA MISSION:
Créer le layout complet et toutes les pages dans {site_dir}/app/ et {site_dir}/components/layout/ avec:
- Header avec navigation responsive
- Footer complet avec infos contact et liens
- Page d'accueil assemblant toutes les sections
- Formulaire de contact multi-étapes avec validation
- Pages légales
- SEO metadata optimisé

═══════════════════════════════════════════════════════════
🧭 COMPOSANT 1: Header.tsx (NAVIGATION)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/layout/Header.tsx:

```typescript
'use client';

import {{ useState, useEffect }} from 'react';
import {{ motion, AnimatePresence }} from 'framer-motion';
import {{ Menu, X, Phone, Mail, ChevronDown }} from 'lucide-react';
import {{ Button }} from '@/components/ui';
import Link from 'next/link';

export function Header() {{
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {{
    const handleScroll = () => {{
      setIsScrolled(window.scrollY > 50);
    }};

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }}, []);

  const navItems = [
    {{ label: 'Accueil', href: '/' }},
    {{ label: 'Services', href: '/#services' }},
    {{ label: 'À Propos', href: '/#about' }},
    {{ label: 'FAQ', href: '/#faq' }},
    {{ label: 'Contact', href: '/#contact' }},
  ];

  return (
    <>
      {{/* Top Bar */}}
      <div className="bg-primary text-white py-2 text-sm hidden md:block">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <a href="tel:{business.get('phone', '')}" className="flex items-center gap-2 hover:text-accent transition-colors">
              <Phone className="h-4 w-4" />
              <span>{business.get('phone', '')}</span>
            </a>
            <a href="mailto:{business.get('email', '')}" className="flex items-center gap-2 hover:text-accent transition-colors">
              <Mail className="h-4 w-4" />
              <span>{business.get('email', '')}</span>
            </a>
          </div>
          <div className="text-white/80">
            {business.get('hours', 'Lun-Ven 8h-18h')}
          </div>
        </div>
      </div>

      {{/* Main Header */}}
      <motion.header
        className={{`sticky top-0 z-50 transition-all duration-300 ${{
          isScrolled
            ? 'bg-white/95 backdrop-blur-md shadow-lg'
            : 'bg-white/80 backdrop-blur-sm'
        }}`}}
        initial={{{{ y: -100 }}}}
        animate={{{{ y: 0 }}}}
        transition={{{{ duration: 0.5 }}}}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            {{/* Logo */}}
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-xl flex items-center justify-center text-white font-black text-xl shadow-lg group-hover:scale-110 transition-transform">
                {business.get('name', '').split(' ')[0][0]}
              </div>
              <div>
                <h1 className="font-black text-xl text-gray-900 group-hover:text-primary transition-colors">
                  {business.get('name', '')}
                </h1>
                <p className="text-xs text-gray-600">{business.get('city', '')}</p>
              </div>
            </Link>

            {{/* Desktop Navigation */}}
            <nav className="hidden lg:flex items-center gap-8">
              {{navItems.map((item) => (
                <a
                  key={{item.href}}
                  href={{item.href}}
                  className="text-gray-700 hover:text-primary font-medium transition-colors relative group"
                >
                  {{item.label}}
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-accent group-hover:w-full transition-all duration-300" />
                </a>
              ))}}
            </nav>

            {{/* Desktop CTA */}}
            <div className="hidden lg:flex items-center gap-4">
              <Button
                variant="primary"
                onClick={{() => document.getElementById('contact-form')?.scrollIntoView({{ behavior: 'smooth' }})}}
              >
                Devis Gratuit
              </Button>
              <Button
                variant="accent"
                leftIcon={{<Phone className="h-5 w-5" />}}
                onClick={{() => window.location.href = 'tel:{business.get('phone', '')}'}}
              >
                Appeler
              </Button>
            </div>

            {{/* Mobile Menu Button */}}
            <button
              onClick={{() => setIsMobileMenuOpen(!isMobileMenuOpen)}}
              className="lg:hidden p-2 text-gray-700 hover:text-primary transition-colors"
              aria-label="Toggle menu"
            >
              {{isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}}
            </button>
          </div>
        </div>
      </motion.header>

      {{/* Mobile Menu */}}
      <AnimatePresence>
        {{isMobileMenuOpen && (
          <motion.div
            initial={{{{ opacity: 0, height: 0 }}}}
            animate={{{{ opacity: 1, height: 'auto' }}}}
            exit={{{{ opacity: 0, height: 0 }}}}
            className="lg:hidden bg-white border-b shadow-lg overflow-hidden fixed top-[72px] md:top-[104px] left-0 right-0 z-40"
          >
            <nav className="px-4 py-6 space-y-4">
              {{navItems.map((item) => (
                <a
                  key={{item.href}}
                  href={{item.href}}
                  onClick={{() => setIsMobileMenuOpen(false)}}
                  className="block py-3 px-4 text-gray-700 hover:bg-primary/5 hover:text-primary rounded-lg font-medium transition-colors"
                >
                  {{item.label}}
                </a>
              ))}}

              <div className="pt-4 space-y-3">
                <Button
                  variant="primary"
                  fullWidth
                  onClick={{() => {{
                    setIsMobileMenuOpen(false);
                    document.getElementById('contact-form')?.scrollIntoView({{ behavior: 'smooth' }});
                  }}}}
                >
                  Devis Gratuit
                </Button>
                <Button
                  variant="accent"
                  fullWidth
                  leftIcon={{<Phone className="h-5 w-5" />}}
                  onClick={{() => window.location.href = 'tel:{business.get('phone', '')}'}}
                >
                  {business.get('phone', '')}
                </Button>
              </div>
            </nav>
          </motion.div>
        )}}
      </AnimatePresence>
    </>
  );
}}
```

═══════════════════════════════════════════════════════════
🔗 COMPOSANT 2: Footer.tsx
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/layout/Footer.tsx:

```typescript
'use client';

import {{ Phone, Mail, MapPin, Clock, Facebook, Instagram, Linkedin }} from 'lucide-react';
import Link from 'next/link';

export function Footer() {{
  const currentYear = new Date().getFullYear();

  const services = `{business.get('services', '')}`.split(',').map(s => s.trim()).slice(0, 4);

  return (
    <footer className="bg-gray-900 text-white">
      {{/* Main Footer */}}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12">
          {{/* Company Info */}}
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-xl flex items-center justify-center text-white font-black text-xl">
                {business.get('name', '').split(' ')[0][0]}
              </div>
              <h3 className="font-black text-xl">{business.get('name', '')}</h3>
            </div>
            <p className="text-gray-400 mb-6 leading-relaxed">
              {business.get('positioning', 'Votre expert local')} depuis {business.get('year', '')}.
            </p>
            <div className="flex gap-4">
              <a href="#" className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center hover:bg-accent transition-colors">
                <Facebook className="h-5 w-5" />
              </a>
              <a href="#" className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center hover:bg-accent transition-colors">
                <Instagram className="h-5 w-5" />
              </a>
              <a href="#" className="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center hover:bg-accent transition-colors">
                <Linkedin className="h-5 w-5" />
              </a>
            </div>
          </div>

          {{/* Services */}}
          <div>
            <h4 className="font-bold text-lg mb-6">Nos Services</h4>
            <ul className="space-y-3">
              {{services.map((service, index) => (
                <li key={{index}}>
                  <a href="/#services" className="text-gray-400 hover:text-accent transition-colors">
                    {{service}}
                  </a>
                </li>
              ))}}
            </ul>
          </div>

          {{/* Links */}}
          <div>
            <h4 className="font-bold text-lg mb-6">Liens Utiles</h4>
            <ul className="space-y-3">
              <li>
                <Link href="/" className="text-gray-400 hover:text-accent transition-colors">
                  Accueil
                </Link>
              </li>
              <li>
                <a href="/#services" className="text-gray-400 hover:text-accent transition-colors">
                  Services
                </a>
              </li>
              <li>
                <a href="/#faq" className="text-gray-400 hover:text-accent transition-colors">
                  FAQ
                </a>
              </li>
              <li>
                <Link href="/mentions-legales" className="text-gray-400 hover:text-accent transition-colors">
                  Mentions Légales
                </Link>
              </li>
              <li>
                <Link href="/politique-confidentialite" className="text-gray-400 hover:text-accent transition-colors">
                  Politique de Confidentialité
                </Link>
              </li>
            </ul>
          </div>

          {{/* Contact */}}
          <div>
            <h4 className="font-bold text-lg mb-6">Contact</h4>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <MapPin className="h-5 w-5 text-accent flex-shrink-0 mt-1" />
                <div className="text-gray-400">
                  {business.get('street', '')}<br />
                  {business.get('postal_code', '')} {business.get('city', '')}
                </div>
              </li>
              <li className="flex items-center gap-3">
                <Phone className="h-5 w-5 text-accent flex-shrink-0" />
                <a href="tel:{business.get('phone', '')}" className="text-gray-400 hover:text-accent transition-colors">
                  {business.get('phone', '')}
                </a>
              </li>
              <li className="flex items-center gap-3">
                <Mail className="h-5 w-5 text-accent flex-shrink-0" />
                <a href="mailto:{business.get('email', '')}" className="text-gray-400 hover:text-accent transition-colors break-all">
                  {business.get('email', '')}
                </a>
              </li>
              <li className="flex items-start gap-3">
                <Clock className="h-5 w-5 text-accent flex-shrink-0 mt-1" />
                <div className="text-gray-400">
                  {business.get('hours', 'Lun-Ven 8h-18h')}
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {{/* Bottom Bar */}}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-gray-400">
            <p>© {{currentYear}} {business.get('name', '')}. Tous droits réservés.</p>
            <p>
              Site créé avec ❤️ par <a href="https://leadgen.lu" className="text-accent hover:underline">Leadgen.lu</a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}}
```

═══════════════════════════════════════════════════════════
📝 COMPOSANT 3: ContactForm.tsx (FORMULAIRE MULTI-ÉTAPES)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/forms/ContactForm.tsx:

```typescript
'use client';

import {{ useState }} from 'react';
import {{ motion, AnimatePresence }} from 'framer-motion';
import {{ useForm }} from 'react-hook-form';
import {{ zodResolver }} from '@hookform/resolvers/zod';
import {{ z }} from 'zod';
import {{ Input, Button, Card }} from '@/components/ui';
import {{ CheckCircle, ArrowRight, ArrowLeft }} from 'lucide-react';

const contactSchema = z.object({{
  name: z.string().min(2, 'Le nom doit contenir au moins 2 caractères'),
  email: z.string().email('Email invalide'),
  phone: z.string().min(8, 'Téléphone invalide'),
  service: z.string().min(1, 'Veuillez sélectionner un service'),
  message: z.string().min(10, 'Le message doit contenir au moins 10 caractères'),
}});

type ContactFormData = z.infer<typeof contactSchema>;

export function ContactForm() {{
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {{
    register,
    handleSubmit,
    formState: {{ errors }},
    trigger,
  }} = useForm<ContactFormData>({{
    resolver: zodResolver(contactSchema),
  }});

  const services = `{business.get('services', '')}`.split(',').map(s => s.trim());

  const nextStep = async () => {{
    let isValid = false;

    if (currentStep === 1) {{
      isValid = await trigger(['name', 'email']);
    }} else if (currentStep === 2) {{
      isValid = await trigger(['phone', 'service']);
    }}

    if (isValid) {{
      setCurrentStep(prev => prev + 1);
    }}
  }};

  const prevStep = () => {{
    setCurrentStep(prev => prev - 1);
  }};

  const onSubmit = async (data: ContactFormData) => {{
    setIsSubmitting(true);

    try {{
      // Simuler l'envoi (à remplacer par votre API)
      await new Promise(resolve => setTimeout(resolve, 2000));

      console.log('Form data:', data);
      setIsSubmitted(true);
    }} catch (error) {{
      console.error('Error submitting form:', error);
      alert('Une erreur est survenue. Veuillez réessayer.');
    }} finally {{
      setIsSubmitting(false);
    }}
  }};

  const steps = [
    {{ number: 1, title: 'Vos coordonnées' }},
    {{ number: 2, title: 'Votre projet' }},
    {{ number: 3, title: 'Détails' }},
  ];

  return (
    <section id="contact-form" className="section-container">
      <div className="max-w-3xl mx-auto">
        {{/* Header */}}
        <div className="text-center mb-12">
          <p className="text-accent font-bold text-lg mb-4">Demande de Devis</p>
          <h2 className="text-h1 font-black mb-6">Obtenez Votre Devis Gratuit</h2>
          <p className="text-body-large text-gray-600">
            Remplissez le formulaire et recevez votre devis personnalisé sous 24h
          </p>
        </div>

        <Card variant="elevated" padding="lg">
          {{!isSubmitted ? (
            <>
              {{/* Progress Steps */}}
              <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                  {{steps.map((step, index) => (
                    <div key={{step.number}} className="flex items-center">
                      <div className={{`flex items-center gap-2 ${{index < steps.length - 1 ? 'flex-1' : ''}}`}}>
                        <div className={{`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all ${{
                          currentStep >= step.number
                            ? 'bg-accent text-white'
                            : 'bg-gray-200 text-gray-600'
                        }}`}}>
                          {{step.number}}
                        </div>
                        <span className={{`hidden sm:inline text-sm font-medium ${{
                          currentStep >= step.number ? 'text-accent' : 'text-gray-600'
                        }}`}}>
                          {{step.title}}
                        </span>
                      </div>
                      {{index < steps.length - 1 && (
                        <div className={{`h-0.5 flex-1 mx-4 transition-all ${{
                          currentStep > step.number ? 'bg-accent' : 'bg-gray-200'
                        }}`}} />
                      )}}
                    </div>
                  ))}}
                </div>
              </div>

              <form onSubmit={{handleSubmit(onSubmit)}}>
                <AnimatePresence mode="wait">
                  {{/* Step 1: Coordonnées */}}
                  {{currentStep === 1 && (
                    <motion.div
                      key="step1"
                      initial={{{{ opacity: 0, x: 20 }}}}
                      animate={{{{ opacity: 1, x: 0 }}}}
                      exit={{{{ opacity: 0, x: -20 }}}}
                      className="space-y-6"
                    >
                      <Input
                        label="Nom complet"
                        placeholder="Jean Dupont"
                        required
                        error={{errors.name?.message}}
                        {{...register('name')}}
                      />

                      <Input
                        label="Email"
                        type="email"
                        placeholder="jean.dupont@example.com"
                        required
                        error={{errors.email?.message}}
                        {{...register('email')}}
                      />

                      <div className="flex justify-end">
                        <Button
                          type="button"
                          variant="accent"
                          rightIcon={{<ArrowRight className="h-5 w-5" />}}
                          onClick={{nextStep}}
                        >
                          Continuer
                        </Button>
                      </div>
                    </motion.div>
                  )}}

                  {{/* Step 2: Projet */}}
                  {{currentStep === 2 && (
                    <motion.div
                      key="step2"
                      initial={{{{ opacity: 0, x: 20 }}}}
                      animate={{{{ opacity: 1, x: 0 }}}}
                      exit={{{{ opacity: 0, x: -20 }}}}
                      className="space-y-6"
                    >
                      <Input
                        label="Téléphone"
                        type="tel"
                        placeholder="+352 661 234 567"
                        required
                        error={{errors.phone?.message}}
                        {{...register('phone')}}
                      />

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Service recherché <span className="text-accent">*</span>
                        </label>
                        <select
                          className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                          {{...register('service')}}
                        >
                          <option value="">Sélectionnez un service</option>
                          {{services.map((service, index) => (
                            <option key={{index}} value={{service}}>{{service}}</option>
                          ))}}
                        </select>
                        {{errors.service && (
                          <p className="mt-1 text-sm text-red-600">{{errors.service.message}}</p>
                        )}}
                      </div>

                      <div className="flex justify-between">
                        <Button
                          type="button"
                          variant="ghost"
                          leftIcon={{<ArrowLeft className="h-5 w-5" />}}
                          onClick={{prevStep}}
                        >
                          Retour
                        </Button>
                        <Button
                          type="button"
                          variant="accent"
                          rightIcon={{<ArrowRight className="h-5 w-5" />}}
                          onClick={{nextStep}}
                        >
                          Continuer
                        </Button>
                      </div>
                    </motion.div>
                  )}}

                  {{/* Step 3: Détails */}}
                  {{currentStep === 3 && (
                    <motion.div
                      key="step3"
                      initial={{{{ opacity: 0, x: 20 }}}}
                      animate={{{{ opacity: 1, x: 0 }}}}
                      exit={{{{ opacity: 0, x: -20 }}}}
                      className="space-y-6"
                    >
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Décrivez votre projet <span className="text-accent">*</span>
                        </label>
                        <textarea
                          rows={{6}}
                          className="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
                          placeholder="Décrivez en détail votre besoin..."
                          {{...register('message')}}
                        />
                        {{errors.message && (
                          <p className="mt-1 text-sm text-red-600">{{errors.message.message}}</p>
                        )}}
                      </div>

                      <div className="flex justify-between">
                        <Button
                          type="button"
                          variant="ghost"
                          leftIcon={{<ArrowLeft className="h-5 w-5" />}}
                          onClick={{prevStep}}
                        >
                          Retour
                        </Button>
                        <Button
                          type="submit"
                          variant="accent"
                          size="lg"
                          isLoading={{isSubmitting}}
                          rightIcon={{<ArrowRight className="h-5 w-5" />}}
                        >
                          {{isSubmitting ? 'Envoi en cours...' : 'Envoyer ma demande'}}
                        </Button>
                      </div>
                    </motion.div>
                  )}}
                </AnimatePresence>
              </form>
            </>
          ) : (
            {{/* Success Message */}}
            <motion.div
              initial={{{{ opacity: 0, scale: 0.9 }}}}
              animate={{{{ opacity: 1, scale: 1 }}}}
              className="text-center py-12"
            >
              <CheckCircle className="h-20 w-20 text-accent mx-auto mb-6" />
              <h3 className="text-h2 font-bold mb-4">Demande Envoyée !</h3>
              <p className="text-gray-600 mb-8">
                Merci pour votre demande. Nous vous répondrons dans les plus brefs délais avec un devis détaillé.
              </p>
              <Button
                variant="accent"
                onClick={{() => {{
                  setIsSubmitted(false);
                  setCurrentStep(1);
                }}}}
              >
                Faire une nouvelle demande
              </Button>
            </motion.div>
          )}}
        </Card>
      </div>
    </section>
  );
}}
```

═══════════════════════════════════════════════════════════
🏠 PAGE 1: app/page.tsx (HOMEPAGE)
═══════════════════════════════════════════════════════════

Crée {site_dir}/app/page.tsx:

```typescript
import {{ Header }} from '@/components/layout/Header';
import {{ Footer }} from '@/components/layout/Footer';
import {{ Hero, Stats, Services, Testimonials, FAQ, FinalCTA }} from '@/components/sections';
import {{ ContactForm }} from '@/components/forms/ContactForm';

export default function HomePage() {{
  return (
    <>
      <Header />
      <main>
        <Hero />
        <Stats />
        <Services />
        <Testimonials />
        <FAQ />
        <ContactForm />
        <FinalCTA />
      </main>
      <Footer />
    </>
  );
}}
```

═══════════════════════════════════════════════════════════
📄 PAGE 2: app/layout.tsx (ROOT LAYOUT)
═══════════════════════════════════════════════════════════

Crée {site_dir}/app/layout.tsx:

```typescript
import type {{ Metadata }} from 'next';
import {{ Inter }} from 'next/font/google';
import './globals.css';

const inter = Inter({{ subsets: ['latin'] }});

export const metadata: Metadata = {{
  title: '{business.get('name', '')} - {business.get('positioning', '')} à {business.get('city', '')}',
  description: `{business.get('services', '')} professionnel à {business.get('city', '')}. {business.get('positioning', '')}. Devis gratuit, intervention rapide. Contactez-nous au {business.get('phone', '')}.`,
  keywords: `{business.get('services', '')}, {business.get('city', '')}, devis gratuit, intervention rapide`,
  authors: [{{ name: '{business.get('name', '')}' }}],
  openGraph: {{
    title: '{business.get('name', '')} - {business.get('positioning', '')}',
    description: `{business.get('services', '')} à {business.get('city', '')}. Devis gratuit.`,
    url: '{business.get('domain_url', '')}',
    siteName: '{business.get('name', '')}',
    locale: 'fr_FR',
    type: 'website',
  }},
  robots: {{
    index: true,
    follow: true,
  }},
  verification: {{
    google: 'your-google-verification-code',
  }},
}};

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode;
}}) {{
  return (
    <html lang="fr">
      <body className={{inter.className}}>{{children}}</body>
    </html>
  );
}}
```

═══════════════════════════════════════════════════════════
📜 PAGE 3: app/(pages)/mentions-legales/page.tsx
═══════════════════════════════════════════════════════════

Crée {site_dir}/app/(pages)/mentions-legales/page.tsx:

```typescript
import {{ Header }} from '@/components/layout/Header';
import {{ Footer }} from '@/components/layout/Footer';

export const metadata = {{
  title: 'Mentions Légales - {business.get('name', '')}',
}};

export default function MentionsLegales() {{
  return (
    <>
      <Header />
      <main className="section-container prose prose-lg mx-auto">
        <h1>Mentions Légales</h1>

        <h2>Éditeur du site</h2>
        <p>
          <strong>{business.get('name', '')}</strong><br />
          {business.get('street', '')}<br />
          {business.get('postal_code', '')} {business.get('city', '')}<br />
          Tél: {business.get('phone', '')}<br />
          Email: {business.get('email', '')}
        </p>

        <h2>Hébergement</h2>
        <p>
          Ce site est hébergé par Vercel Inc.<br />
          340 S Lemon Ave #4133<br />
          Walnut, CA 91789<br />
          United States
        </p>

        <h2>Propriété intellectuelle</h2>
        <p>
          L'ensemble du contenu de ce site (textes, images, vidéos) est la propriété de {business.get('name', '')}.
          Toute reproduction, même partielle, est interdite sans autorisation préalable.
        </p>

        <h2>Responsabilité</h2>
        <p>
          Les informations contenues sur ce site sont aussi précises que possible mais peuvent contenir des inexactitudes.
          {business.get('name', '')} ne pourra être tenue responsable des dommages directs ou indirects causés au matériel
          de l'utilisateur lors de l'accès au site.
        </p>
      </main>
      <Footer />
    </>
  );
}}
```

═══════════════════════════════════════════════════════════
🔒 PAGE 4: app/(pages)/politique-confidentialite/page.tsx
═══════════════════════════════════════════════════════════

Crée {site_dir}/app/(pages)/politique-confidentialite/page.tsx:

```typescript
import {{ Header }} from '@/components/layout/Header';
import {{ Footer }} from '@/components/layout/Footer';

export const metadata = {{
  title: 'Politique de Confidentialité - {business.get('name', '')}',
}};

export default function PolitiqueConfidentialite() {{
  return (
    <>
      <Header />
      <main className="section-container prose prose-lg mx-auto">
        <h1>Politique de Confidentialité</h1>

        <h2>Collecte des données</h2>
        <p>
          Nous collectons les données personnelles que vous nous fournissez volontairement via notre formulaire de contact:
          nom, email, téléphone, et message. Ces données sont uniquement utilisées pour répondre à votre demande.
        </p>

        <h2>Utilisation des données</h2>
        <p>
          Vos données personnelles sont utilisées exclusivement pour:
        </p>
        <ul>
          <li>Répondre à vos demandes de devis</li>
          <li>Vous contacter concernant nos services</li>
          <li>Améliorer notre service client</li>
        </ul>

        <h2>Protection des données</h2>
        <p>
          Nous mettons en œuvre des mesures de sécurité appropriées pour protéger vos données contre tout accès,
          modification, divulgation ou destruction non autorisés.
        </p>

        <h2>Vos droits</h2>
        <p>
          Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement et de portabilité
          de vos données. Pour exercer ces droits, contactez-nous à {business.get('email', '')}.
        </p>

        <h2>Cookies</h2>
        <p>
          Ce site n'utilise pas de cookies de traçage. Seuls des cookies techniques essentiels au fonctionnement
          du site peuvent être utilisés.
        </p>

        <h2>Contact</h2>
        <p>
          Pour toute question concernant cette politique, contactez-nous:<br />
          Email: {business.get('email', '')}<br />
          Téléphone: {business.get('phone', '')}
        </p>
      </main>
      <Footer />
    </>
  );
}}
```

═══════════════════════════════════════════════════════════
📦 EXPORTS
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/layout/index.ts:

```typescript
export {{ Header }} from './Header';
export {{ Footer }} from './Footer';
```

Crée {site_dir}/components/forms/index.ts:

```typescript
export {{ ContactForm }} from './ContactForm';
```

═══════════════════════════════════════════════════════════
✅ CRITÈRES DE SUCCÈS
═══════════════════════════════════════════════════════════

Vérifie que :
✓ Header avec navigation responsive créé
✓ Footer complet avec liens et infos contact créé
✓ ContactForm multi-étapes avec validation Zod créé
✓ Page d'accueil assemblant toutes les sections créée
✓ Layout root avec metadata SEO créé
✓ Pages légales (mentions + confidentialité) créées
✓ Structure de dossiers app/(pages)/ créée
✓ Tous les exports centralisés créés
✓ Navigation mobile fonctionnelle
✓ Formulaire multi-étapes avec progress indicator
✓ Aucune erreur TypeScript

Une fois terminé, réponds avec:
- Liste des composants layout créés (Header, Footer)
- Liste des pages créées (homepage, légales)
- Confirmation formulaire multi-étapes fonctionnel
- Prêt pour Phase 5 (Content/SEO)"""
