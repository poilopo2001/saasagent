"""
Site Validator Agent - Valide la qualité et la production-readiness du site généré
"""


class SiteValidatorAgent:
    """Agent spécialisé dans la validation multi-critères de sites Next.js"""

    @staticmethod
    def get_validation_prompt(site_dir: str, attempt: int, max_attempts: int) -> str:
        """
        Génère le prompt de validation pour Claude Code SDK

        Args:
            site_dir: Chemin du répertoire du site à valider
            attempt: Numéro de tentative actuelle
            max_attempts: Nombre maximum de tentatives

        Returns:
            Le prompt de validation
        """
        return f"""Tu es l'agent site-validator-pro. Valide ce site Next.js généré pour garantir sa production-readiness.

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
- Indique clairement SAFE TO DEPLOY ou FAILED

Tentative {attempt}/{max_attempts}"""

    @staticmethod
    def get_fix_prompt(site_dir: str, validation_report: str, attempt: int) -> str:
        """
        Génère le prompt de correction automatique

        Args:
            site_dir: Chemin du répertoire du site
            validation_report: Rapport de validation contenant les erreurs
            attempt: Numéro de tentative actuelle

        Returns:
            Le prompt de correction
        """
        return f"""Tu as généré un site Next.js qui présente des erreurs de validation. Tu dois CORRIGER tous les problèmes détectés.

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
