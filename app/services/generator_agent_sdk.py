"""
Generator Service avec Claude Agent SDK v0.1.0 - Architecture Optimale

Utilise TOUTES les capacités du nouveau SDK :
- claude-agent-sdk (nouveau nom officiel)
- ClaudeAgentOptions avec agents définis programmatiquement
- ClaudeSDKClient pour conversation continue
- System prompt Claude Code preset
- Hooks pour monitoring en temps réel
- Permissions customisées
- Gestion d'erreurs avancée
"""
import os
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    ResultMessage,
    HookMatcher,
    HookContext,
    CLINotFoundError,
    ProcessError,
    ClaudeSDKError
)

from app.core.config import get_settings
from app.services.job_manager import job_manager
from app.agents.modular import (
    SetupAgent,
    ComponentAgent,
    SectionAgent,
    PageAgent,
    ContentAgent
)

logger = logging.getLogger(__name__)
settings = get_settings()


class GeneratorServiceAgentSDK:
    """
    Service avec Claude Agent SDK v0.1.0 - Architecture Optimale

    Utilise le vrai système multi-agents du SDK avec :
    - Agents définis programmatiquement dans ClaudeAgentOptions
    - Claude lance automatiquement les sous-agents via Task tool
    - Conversation continue avec ClaudeSDKClient
    - Hooks pour monitoring temps réel
    - System prompt Claude Code
    """

    @staticmethod
    async def run_generation_workflow(job_id: str, business_data: Dict[str, Any], site_slug: str):
        """
        Exécute le workflow avec l'architecture Agent SDK optimale

        Architecture :
        1. Définit les 5 agents spécialisés dans ClaudeAgentOptions
        2. Claude Code système prompt activé
        3. ClaudeSDKClient pour conversation continue
        4. Hooks pour monitoring en temps réel
        5. Claude gère automatiquement le parallélisme

        Args:
            job_id: ID du job
            business_data: Données business
            site_slug: Slug du site
        """
        site_dir = f"{settings.output_dir}/{site_slug}"

        try:
            job_manager.update_job(job_id, "processing", 0, "🚀 Démarrage Agent SDK v0.1.0...")

            # Créer le répertoire
            os.makedirs(site_dir, exist_ok=True)

            # Définir les agents programmatiquement
            agents_config = GeneratorServiceAgentSDK._create_agents_config(
                business_data, site_slug, site_dir
            )

            # Configuration complète du SDK
            options = ClaudeAgentOptions(
                # System prompt Claude Code officiel
                system_prompt={"type": "preset", "preset": "claude_code"},

                # Agents définis programmatiquement
                agents=agents_config,

                # Outils autorisés
                allowed_tools=["Task", "Read", "Write", "Edit", "Bash", "Glob", "Grep"],

                # Mode permission
                permission_mode="acceptEdits",

                # Répertoire de travail
                cwd=site_dir,

                # Charger settings projet (CLAUDE.md si présent)
                setting_sources=["project"],

                # Modèle
                model=settings.agent_model,

                # Hooks pour monitoring
                hooks=GeneratorServiceAgentSDK._create_hooks(job_id),

                # Permissions customisées
                can_use_tool=GeneratorServiceAgentSDK._custom_permission_handler,

                # Inclure messages partiels pour streaming
                include_partial_messages=False
            )

            # Lancer la génération avec ClaudeSDKClient
            await GeneratorServiceAgentSDK._execute_generation(
                job_id, business_data, site_slug, site_dir, options
            )

            job_manager.update_job(
                job_id, "completed", 100,
                "✅ Génération Agent SDK terminée!"
            )

        except CLINotFoundError as e:
            error_msg = "Claude Code CLI non trouvé. Installer avec: npm install -g @anthropic-ai/claude-code"
            logger.error(f"CLI not found: {str(e)}")
            job_manager.update_job(
                job_id, "failed", 0, f"❌ {error_msg}",
                error=str(e)
            )

        except ProcessError as e:
            error_msg = f"Erreur process (exit code {e.exit_code}): {e.stderr}"
            logger.error(error_msg)
            job_manager.update_job(
                job_id, "failed", 0, f"❌ {error_msg}",
                error=str(e)
            )

        except ClaudeSDKError as e:
            logger.error(f"Erreur SDK job {job_id}: {str(e)}", exc_info=True)
            job_manager.update_job(
                job_id, "failed", 0, f"❌ Erreur SDK: {str(e)}",
                error=str(e)
            )

        except Exception as e:
            logger.error(f"Erreur job {job_id}: {str(e)}", exc_info=True)
            job_manager.update_job(
                job_id, "failed", 0, f"❌ Échec: {str(e)}",
                error=str(e)
            )

    @staticmethod
    def _create_agents_config(business_data: Dict[str, Any], site_slug: str, site_dir: str) -> Dict[str, Dict[str, Any]]:
        """
        Créer la configuration des agents programmatiquement

        Claude va automatiquement lancer ces agents via Task tool
        quand le prompt principal mentionne leurs noms ou descriptions
        """
        return {
            "setup": {
                "description": "Setup Next.js 14 project structure with Tailwind CSS, TypeScript, and all config files",
                "prompt": SetupAgent.get_prompt(business_data, site_slug, site_dir),
                "tools": ["Write", "Bash", "Read", "Edit"],
                "model": "sonnet"
            },
            "components": {
                "description": "Create reusable UI components (Button, Input, Card, Accordion, Tabs) with Framer Motion animations",
                "prompt": ComponentAgent.get_prompt(business_data, site_slug, site_dir),
                "tools": ["Write", "Read", "Edit"],
                "model": "sonnet"
            },
            "sections": {
                "description": "Build homepage sections (Hero, Stats, Services, Testimonials, FAQ, FinalCTA) with responsive design",
                "prompt": SectionAgent.get_prompt(business_data, site_slug, site_dir),
                "tools": ["Write", "Read", "Edit"],
                "model": "sonnet"
            },
            "pages": {
                "description": "Create complete pages (Header, Footer, Contact form, Homepage, Legal pages) using components and sections",
                "prompt": PageAgent.get_prompt(business_data, site_slug, site_dir),
                "tools": ["Write", "Read", "Edit"],
                "model": "sonnet"
            },
            "content": {
                "description": "Generate SEO metadata, JSON-LD schemas, sitemap, robots.txt, and optimize content",
                "prompt": ContentAgent.get_prompt(business_data, site_slug, site_dir),
                "tools": ["Write", "Read", "Edit"],
                "model": "sonnet"
            }
        }

    @staticmethod
    def _create_hooks(job_id: str) -> Dict[str, list]:
        """
        Créer les hooks pour monitoring en temps réel

        Hooks disponibles :
        - PreToolUse: Avant exécution d'un outil
        - PostToolUse: Après exécution d'un outil
        - UserPromptSubmit: Quand un prompt est envoyé
        - Stop: Quand l'exécution s'arrête
        - SubagentStop: Quand un sous-agent termine
        """

        async def pre_tool_hook(input_data: Dict[str, Any], tool_use_id: Optional[str], context: HookContext) -> Dict[str, Any]:
            """Hook appelé avant chaque utilisation d'outil"""
            tool_name = input_data.get('tool_name', 'unknown')
            logger.info(f"[Job {job_id}] 🔧 Tool à utiliser: {tool_name}")

            # Mettre à jour le job selon l'outil
            if tool_name == "Task":
                tool_input = input_data.get('tool_input', {})
                subagent_type = tool_input.get('subagent_type', 'unknown')
                description = tool_input.get('description', '')
                logger.info(f"[Job {job_id}] 🤖 Lancement sous-agent: {subagent_type} - {description}")
                job_manager.update_job(job_id, "processing", None, f"🤖 Agent: {description}")

            return {}

        async def post_tool_hook(input_data: Dict[str, Any], tool_use_id: Optional[str], context: HookContext) -> Dict[str, Any]:
            """Hook appelé après chaque utilisation d'outil"""
            tool_name = input_data.get('tool_name', 'unknown')
            logger.info(f"[Job {job_id}] ✅ Tool terminé: {tool_name}")
            return {}

        async def subagent_stop_hook(input_data: Dict[str, Any], tool_use_id: Optional[str], context: HookContext) -> Dict[str, Any]:
            """Hook appelé quand un sous-agent termine"""
            agent_type = input_data.get('subagent_type', 'unknown')
            logger.info(f"[Job {job_id}] ✅ Sous-agent terminé: {agent_type}")
            return {}

        return {
            'PreToolUse': [
                HookMatcher(hooks=[pre_tool_hook])
            ],
            'PostToolUse': [
                HookMatcher(hooks=[post_tool_hook])
            ],
            'SubagentStop': [
                HookMatcher(hooks=[subagent_stop_hook])
            ]
        }

    @staticmethod
    async def _custom_permission_handler(tool_name: str, input_data: dict, context: dict) -> dict:
        """
        Handler customisé pour permissions

        Permet de bloquer certaines opérations dangereuses
        ou de rediriger des fichiers sensibles
        """

        # Bloquer suppressions système
        if tool_name == "Bash":
            command = input_data.get("command", "")
            if "rm -rf /" in command or "rm -rf /*" in command:
                return {
                    "behavior": "deny",
                    "message": "Commande système dangereuse bloquée",
                    "interrupt": True
                }

        # Rediriger fichiers .env vers .env.example
        if tool_name in ["Write", "Edit"]:
            file_path = input_data.get("file_path", "")
            if file_path.endswith(".env") and not file_path.endswith(".env.example"):
                logger.warning(f"Tentative d'écriture .env redirigée vers .env.example")
                return {
                    "behavior": "allow",
                    "updatedInput": {
                        **input_data,
                        "file_path": file_path + ".example"
                    }
                }

        # Autoriser tout le reste
        return {
            "behavior": "allow",
            "updatedInput": input_data
        }

    @staticmethod
    async def _execute_generation(
        job_id: str,
        business_data: Dict[str, Any],
        site_slug: str,
        site_dir: str,
        options: ClaudeAgentOptions
    ):
        """
        Exécuter la génération avec ClaudeSDKClient

        Utilise une conversation continue où Claude gère automatiquement
        les sous-agents et le parallélisme
        """
        business_name = business_data.get('name', 'Business')
        business_city = business_data.get('city', 'City')
        services = business_data.get('services', 'Services divers')

        # Prompt principal optimisé pour Claude Agent SDK
        main_prompt = f"""Tu es un expert en génération de sites web Next.js 14.

🎯 MISSION : Générer un site web professionnel complet pour {business_name} à {business_city}

📋 DONNÉES BUSINESS :
- Entreprise : {business_name}
- Localisation : {business_city}
- Services : {services}
- Contact : {business_data.get('phone', 'N/A')} | {business_data.get('email', 'N/A')}
- Positionnement : {business_data.get('positioning', 'Entreprise locale professionnelle')}

🤖 AGENTS DISPONIBLES :
Tu as accès à 5 agents spécialisés que tu DOIS utiliser dans cet ordre :

1. **setup** : Crée la structure Next.js 14 (package.json, tailwind, tsconfig, npm install)
2. **components** : Génère les composants UI réutilisables (Button, Input, Card, etc.)
3. **sections** : Construit les sections homepage (Hero, Services, Testimonials, FAQ, CTA)
4. **pages** : Assemble les pages complètes (Header, Footer, Homepage, Contact, Légales)
5. **content** : Optimise SEO (metadata, JSON-LD, sitemap, robots.txt)

⚡ WORKFLOW OPTIMAL :
- Phase 1 : Lance l'agent **setup** (SEUL - crée la base)
- Phase 2+3 : Lance EN PARALLÈLE les agents **components** ET **sections** (indépendants)
- Phase 4 : Lance l'agent **pages** (utilise les résultats de 2+3)
- Phase 5 : Lance l'agent **content** (finale)

📂 RÉPERTOIRE : {site_dir}

✅ CRITÈRES DE SUCCÈS :
- Site Next.js 14 fonctionnel avec npm run dev
- Design moderne avec Tailwind CSS et Framer Motion
- Composants réutilisables avec TypeScript
- SEO optimisé avec metadata et schemas
- Formulaire de contact multi-étapes
- Responsive mobile-first
- Accessibilité WCAG AA

🚀 COMMENCE MAINTENANT en utilisant les agents spécialisés.
Travaille de manière AUTONOME et utilise le Task tool pour lancer les agents.
"""

        async with ClaudeSDKClient(options=options) as client:
            # Lancer la génération
            job_manager.update_job(job_id, "processing", 5, "🎬 Démarrage génération...")
            await client.query(main_prompt)

            # Suivre la progression
            current_phase = 1
            total_phases = 5

            async for message in client.receive_messages():
                # Traiter les messages
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            # Logger le texte de Claude
                            logger.info(f"[Job {job_id}] Claude: {block.text[:200]}...")

                        elif isinstance(block, ToolUseBlock):
                            # Un outil est utilisé
                            if block.name == "Task":
                                # Un sous-agent est lancé
                                description = block.input.get('description', 'Agent')
                                logger.info(f"[Job {job_id}] 🤖 Lancement: {description}")

                                # Calculer progression
                                progress = int((current_phase / total_phases) * 80)
                                job_manager.update_job(
                                    job_id, "processing", progress,
                                    f"🤖 Phase {current_phase}/{total_phases}: {description}"
                                )

                        elif isinstance(block, ToolResultBlock):
                            # Résultat d'outil reçu
                            if block.is_error:
                                logger.error(f"[Job {job_id}] ❌ Erreur outil: {block.content}")

                elif isinstance(message, ResultMessage):
                    # Message final
                    logger.info(f"[Job {job_id}] 🎯 Résultat final:")
                    logger.info(f"  - Durée: {message.duration_ms}ms")
                    logger.info(f"  - Tours: {message.num_turns}")
                    logger.info(f"  - Coût: ${message.total_cost_usd or 0:.4f}")
                    logger.info(f"  - Session: {message.session_id}")

                    if message.is_error:
                        raise Exception(f"Génération échouée: {message.result}")

                    # Succès !
                    job_manager.update_job(
                        job_id, "processing", 95,
                        "✅ Génération terminée, finalisation..."
                    )
                    break

            # Finaliser
            job_manager.update_job(
                job_id, "processing", 100,
                "✅ Site généré avec succès!"
            )
