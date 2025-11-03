"""
Modular Agents - Architecture 5 phases
Chaque phase génère une partie spécifique du site Next.js
"""

from .phase1_setup import SetupAgent
from .phase2_components import ComponentAgent
from .phase3_sections import SectionAgent
from .phase4_pages import PageAgent
from .phase5_content import ContentAgent

__all__ = [
    'SetupAgent',
    'ComponentAgent',
    'SectionAgent',
    'PageAgent',
    'ContentAgent',
]
