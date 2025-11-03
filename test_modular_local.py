"""
Test script pour verifier le systeme modulaire en local
"""
import os
import json
import asyncio
from app.services.generator_modular import GeneratorServiceModular
from app.core.config import get_settings

settings = get_settings()

async def test_phases():
    print("=== TEST SYSTEME MODULAIRE 5 PHASES ===\n")
    
    # Donnees de test
    business_data = {
        "name": "Test Plomberie",
        "location": "Luxembourg",
        "phone": "661234567",
        "email": "test@plomberie.lu",
        "year": 2020,
        "services": "Depannage urgence, Installation sanitaire, Reparation fuites",
        "positioning": "Expert plomberie 24h/7j a Luxembourg",
        "street": "1 rue Test",
        "postal_code": "L-1234",
        "city": "Luxembourg"
    }
    
    site_slug = "test-plomberie-luxembourg"
    site_dir = f"./tmp/generated-sites/{site_slug}"
    
    print(f"Site directory: {site_dir}")
    print(f"Business: {business_data['name']} - {business_data['city']}\n")
    
    # Test de chaque agent
    from app.agents.modular import SetupAgent, ComponentAgent, SectionAgent, PageAgent, ContentAgent
    
    agents = [
        ("Phase 1: Setup", SetupAgent),
        ("Phase 2: Components", ComponentAgent),
        ("Phase 3: Sections", SectionAgent),
        ("Phase 4: Pages", PageAgent),
        ("Phase 5: Content", ContentAgent)
    ]
    
    for phase_name, agent_class in agents:
        print(f"\n--- {phase_name} ---")
        try:
            prompt = agent_class.get_prompt(business_data, site_slug, site_dir)
            prompt_length = len(prompt)
            print(f"OK: Prompt genere ({prompt_length} caracteres)")
            
            # Afficher un apercu du prompt
            lines = prompt.split('\n')
            print(f"Premiere ligne: {lines[0][:80]}...")
            print(f"Derniere ligne: {lines[-1][:80]}...")
        except Exception as e:
            print(f"ERREUR: {str(e)}")
            return False
    
    print("\n=== TOUS LES AGENTS SONT OPERATIONNELS ===")
    return True

if __name__ == "__main__":
    result = asyncio.run(test_phases())
    exit(0 if result else 1)
