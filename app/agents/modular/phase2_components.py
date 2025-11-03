"""
Phase 2: Component Agent - Composants UI de base réutilisables
Génère TOUS les composants UI fondamentaux avec design system complet
"""
from typing import Dict, Any


class ComponentAgent:
    """Agent Phase 2: Composants UI de base avec design system"""

    @staticmethod
    def get_prompt(business: Dict[str, Any], site_slug: str, site_dir: str) -> str:
        """
        Génère le prompt de création des composants UI

        Ce prompt est ENRICHI avec :
        - Tous les states des composants (hover, active, disabled, loading)
        - Accessibilité complète (ARIA labels, keyboard navigation)
        - Responsive design parfait
        - Animations Framer Motion intégrées
        - TypeScript types stricts
        """
        return f"""Tu es l'agent Component spécialisé dans la création de composants UI modernes, accessibles et performants.

📋 CONTEXTE:
Tu travailles sur le projet dans {site_dir}
La Phase 1 (Setup) est TERMINÉE - tous les fichiers de config existent.
Les couleurs primary et accent sont déjà définies dans tailwind.config.js.

🎯 TA MISSION:
Créer TOUS les composants UI de base dans {site_dir}/components/ui/ avec:
- Design system cohérent
- Tous les états (default, hover, active, focus, disabled, loading)
- Accessibilité WCAG AA minimum
- TypeScript strict
- Animations Framer Motion smooth
- Documentation JSDoc complète

═══════════════════════════════════════════════════════════
🔘 COMPOSANT 1: Button.tsx (ULTRA-COMPLET)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/ui/Button.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ Loader2 }} from 'lucide-react';
import {{ ButtonHTMLAttributes, forwardRef }} from 'react';
import {{ cn }} from '@/lib/utils';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {{
  variant?: 'primary' | 'accent' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {{
      className,
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      disabled,
      children,
      ...props
    }},
    ref
  ) => {{
    const baseStyles = 'inline-flex items-center justify-center gap-2 font-semibold rounded-lg transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

    const variants = {{
      primary: 'bg-primary text-white shadow-xl hover:bg-primary-600 hover:scale-105 active:scale-95 focus:ring-primary',
      accent: 'bg-accent text-white shadow-glow hover:shadow-glow-lg hover:bg-accent-600 focus:ring-accent',
      secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 active:bg-gray-300 focus:ring-gray-500',
      outline: 'border-2 border-primary text-primary hover:bg-primary hover:text-white focus:ring-primary',
      ghost: 'text-primary hover:bg-primary-50 active:bg-primary-100 focus:ring-primary',
    }};

    const sizes = {{
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-6 py-3 text-base',
      lg: 'px-8 py-4 text-lg',
      xl: 'px-10 py-5 text-xl',
    }};

    return (
      <motion.button
        ref={{ref}}
        className={{cn(
          baseStyles,
          variants[variant],
          sizes[size],
          fullWidth && 'w-full',
          className
        )}}
        disabled={{disabled || isLoading}}
        whileHover={{{{ scale: disabled || isLoading ? 1 : 1.02 }}}}
        whileTap={{{{ scale: disabled || isLoading ? 1 : 0.98 }}}}
        {{...props}}
      >
        {{isLoading && <Loader2 className="h-5 w-5 animate-spin" />}}
        {{!isLoading && leftIcon && leftIcon}}
        {{children}}
        {{!isLoading && rightIcon && rightIcon}}
      </motion.button>
    );
  }}
);

Button.displayName = 'Button';

export {{ Button }};
```

═══════════════════════════════════════════════════════════
📝 COMPOSANT 2: Input.tsx (FORMULAIRES)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/ui/Input.tsx:

```typescript
'use client';

import {{ forwardRef, InputHTMLAttributes }} from 'react';
import {{ cn }} from '@/lib/utils';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {{
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({{ className, label, error, helperText, leftIcon, rightIcon, ...props }}, ref) => {{
    return (
      <div className="w-full">
        {{label && (
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {{label}}
            {{props.required && <span className="text-accent ml-1">*</span>}}
          </label>
        )}}

        <div className="relative">
          {{leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              {{leftIcon}}
            </div>
          )}}

          <input
            ref={{ref}}
            className={{cn(
              'w-full px-4 py-3 rounded-lg border border-gray-300 bg-white',
              'text-gray-900 placeholder:text-gray-400',
              'focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
              'transition-all duration-200',
              'disabled:bg-gray-50 disabled:cursor-not-allowed',
              error && 'border-red-500 focus:ring-red-500',
              leftIcon && 'pl-10',
              rightIcon && 'pr-10',
              className
            )}}
            {{...props}}
          />

          {{rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
              {{rightIcon}}
            </div>
          )}}
        </div>

        {{error && (
          <p className="mt-1 text-sm text-red-600">{{error}}</p>
        )}}

        {{helperText && !error && (
          <p className="mt-1 text-sm text-gray-500">{{helperText}}</p>
        )}}
      </div>
    );
  }}
);

Input.displayName = 'Input';

export {{ Input }};
```

═══════════════════════════════════════════════════════════
🎴 COMPOSANT 3: Card.tsx
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/ui/Card.tsx:

```typescript
'use client';

import {{ motion }} from 'framer-motion';
import {{ HTMLAttributes, forwardRef }} from 'react';
import {{ cn }} from '@/lib/utils';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {{
  variant?: 'default' | 'bordered' | 'elevated' | 'glass';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
}}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({{ className, variant = 'default', padding = 'md', hover = true, children, ...props }}, ref) => {{
    const variants = {{
      default: 'bg-white',
      bordered: 'bg-white border border-gray-200',
      elevated: 'bg-white shadow-lg',
      glass: 'bg-white/10 backdrop-blur-md border border-white/20',
    }};

    const paddings = {{
      none: '',
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8',
    }};

    return (
      <motion.div
        ref={{ref}}
        className={{cn(
          'rounded-2xl transition-all duration-500',
          variants[variant],
          paddings[padding],
          hover && 'hover:shadow-2xl hover:border-accent',
          className
        )}}
        whileHover={{hover ? {{ y: -5 }} : {{}}}}
        {{...props}}
      >
        {{children}}
      </motion.div>
    );
  }}
);

Card.displayName = 'Card';

export {{ Card }};
```

═══════════════════════════════════════════════════════════
📊 COMPOSANT 4: Accordion.tsx (FAQ)
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/ui/Accordion.tsx:

```typescript
'use client';

import {{ useState }} from 'react';
import {{ motion, AnimatePresence }} from 'framer-motion';
import {{ ChevronDown }} from 'lucide-react';
import {{ cn }} from '@/lib/utils';

export interface AccordionItem {{
  id: string;
  question: string;
  answer: string;
}}

export interface AccordionProps {{
  items: AccordionItem[];
  allowMultiple?: boolean;
  className?: string;
}}

export function Accordion({{ items, allowMultiple = false, className }}: AccordionProps) {{
  const [openItems, setOpenItems] = useState<string[]>([]);

  const toggleItem = (id: string) => {{
    if (allowMultiple) {{
      setOpenItems(prev =>
        prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
      );
    }} else {{
      setOpenItems(prev => (prev.includes(id) ? [] : [id]));
    }}
  }};

  return (
    <div className={{cn('space-y-4', className)}}>
      {{items.map((item) => {{
        const isOpen = openItems.includes(item.id);

        return (
          <div
            key={{item.id}}
            className="bg-white rounded-2xl border border-gray-100 overflow-hidden hover:border-accent transition-colors duration-300"
          >
            <button
              onClick={{() => toggleItem(item.id)}}
              className="w-full flex items-center justify-between p-6 text-left hover:bg-gray-50 transition-colors"
              aria-expanded={{isOpen}}
            >
              <span className="text-lg font-bold text-gray-900 pr-4">
                {{item.question}}
              </span>
              <motion.div
                animate={{{{ rotate: isOpen ? 180 : 0 }}}}
                transition={{{{ duration: 0.3 }}}}
              >
                <ChevronDown className="h-6 w-6 text-accent flex-shrink-0" />
              </motion.div>
            </button>

            <AnimatePresence initial={{false}}>
              {{isOpen && (
                <motion.div
                  initial={{{{ height: 0, opacity: 0 }}}}
                  animate={{{{ height: 'auto', opacity: 1 }}}}
                  exit={{{{ height: 0, opacity: 0 }}}}
                  transition={{{{ duration: 0.3, ease: 'easeInOut' }}}}
                  className="overflow-hidden"
                >
                  <div className="px-6 pb-6 text-gray-700 leading-relaxed">
                    {{item.answer}}
                  </div>
                </motion.div>
              )}}
            </AnimatePresence>
          </div>
        );
      }})}}
    </div>
  );
}}
```

═══════════════════════════════════════════════════════════
📑 COMPOSANT 5: Tabs.tsx
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/ui/Tabs.tsx:

```typescript
'use client';

import {{ useState, ReactNode }} from 'react';
import {{ motion }} from 'framer-motion';
import {{ cn }} from '@/lib/utils';

export interface Tab {{
  id: string;
  label: string;
  content: ReactNode;
}}

export interface TabsProps {{
  tabs: Tab[];
  defaultTab?: string;
  className?: string;
}}

export function Tabs({{ tabs, defaultTab, className }}: TabsProps) {{
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const activeContent = tabs.find(tab => tab.id === activeTab)?.content;

  return (
    <div className={{cn('w-full', className)}}>
      <div className="flex space-x-2 border-b border-gray-200 mb-8">
        {{tabs.map((tab) => {{
          const isActive = tab.id === activeTab;

          return (
            <button
              key={{tab.id}}
              onClick={{() => setActiveTab(tab.id)}}
              className={{cn(
                'relative px-6 py-3 font-semibold transition-colors',
                isActive ? 'text-accent' : 'text-gray-600 hover:text-gray-900'
              )}}
            >
              {{tab.label}}

              {{isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent"
                  transition={{{{ type: 'spring', stiffness: 500, damping: 30 }}}}
                />
              )}}
            </button>
          );
        }})}}
      </div>

      <motion.div
        key={{activeTab}}
        initial={{{{ opacity: 0, y: 10 }}}}
        animate={{{{ opacity: 1, y: 0 }}}}
        transition={{{{ duration: 0.3 }}}}
      >
        {{activeContent}}
      </motion.div>
    </div>
  );
}}
```

═══════════════════════════════════════════════════════════
🛠️ UTILITAIRE: lib/utils.ts (cn helper)
═══════════════════════════════════════════════════════════

Crée {site_dir}/lib/utils.ts:

```typescript
import {{ type ClassValue, clsx }} from 'clsx';
import {{ twMerge }} from 'tailwind-merge';

/**
 * Fonction utilitaire pour merger les classes Tailwind
 * Gère les conflits et optimise les classes
 */
export function cn(...inputs: ClassValue[]) {{
  return twMerge(clsx(inputs));
}}
```

═══════════════════════════════════════════════════════════
📦 EXPORT CENTRALISÉ
═══════════════════════════════════════════════════════════

Crée {site_dir}/components/ui/index.ts:

```typescript
export {{ Button }} from './Button';
export {{ Input }} from './Input';
export {{ Card }} from './Card';
export {{ Accordion }} from './Accordion';
export {{ Tabs }} from './Tabs';

export type {{ ButtonProps }} from './Button';
export type {{ InputProps }} from './Input';
export type {{ CardProps }} from './Card';
export type {{ AccordionItem, AccordionProps }} from './Accordion';
export type {{ Tab, TabsProps }} from './Tabs';
```

═══════════════════════════════════════════════════════════
✅ CRITÈRES DE SUCCÈS
═══════════════════════════════════════════════════════════

Vérifie que :
✓ Tous les 5 composants UI sont créés
✓ Chaque composant a TypeScript strict (interfaces exportées)
✓ Framer Motion intégré pour animations smooth
✓ Accessibilité complète (ARIA, keyboard navigation)
✓ Tous les états gérés (hover, active, disabled, loading)
✓ lib/utils.ts créé avec cn helper
✓ components/ui/index.ts créé pour exports centralisés
✓ Aucune erreur TypeScript

Une fois terminé, réponds avec:
- Liste des 5 composants créés
- Confirmation que lib/utils.ts existe
- Prêt pour Phase 3 (Sections)"""
