# Comparaison Architectures: Modulaire vs Multi-Agents

## 🏗️ ARCHITECTURE ACTUELLE (Modulaire - Sequential)

```
┌─────────────────────────────────────────────────────────┐
│          GeneratorServiceModular (Python)               │
│                 Orchestrateur Séquentiel                │
└─────────────────────────────────────────────────────────┘
                        │
                        ↓
         ┌──────────────────────────────────┐
         │   1 seul Agent Claude (SDK)      │
         │   Exécute tout séquentiellement  │
         └──────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬─────────────┬─────────────┐
        ↓               ↓               ↓             ↓             ↓
    ┌──────┐       ┌──────┐       ┌──────┐      ┌──────┐      ┌──────┐
    │Phase1│       │Phase2│       │Phase3│      │Phase4│      │Phase5│
    │Setup │  →    │Comp. │  →    │Sect. │  →   │Pages │  →   │Content│
    │      │       │      │       │      │      │      │      │       │
    └──────┘       └──────┘       └──────┘      └──────┘      └──────┘
     0-8%          8-16%          16-24%        24-32%        32-40%
```

### Fonctionnement:
1. Python génère `prompt1 = SetupAgent.get_prompt()`
2. Claude reçoit prompt1 → exécute → termine
3. Python génère `prompt2 = ComponentAgent.get_prompt()`
4. Claude reçoit prompt2 → exécute → termine
5. etc.

### Caractéristiques:
- ✅ Simple à comprendre
- ✅ Facile à débugger (linéaire)
- ❌ Lent (séquentiel, pas de parallélisme)
- ❌ 1 seul contexte Claude (limité)
- ❌ Si une phase échoue, tout s'arrête

---

## 🚀 NOUVELLE ARCHITECTURE (Multi-Agents - Parallel)

```
┌─────────────────────────────────────────────────────────┐
│       GeneratorServiceMultiAgent (Python)               │
│         Orchestrateur Multi-Agents Parallèle            │
└─────────────────────────────────────────────────────────┘
                        │
                        ↓
         ┌──────────────────────────────────┐
         │  Agent Claude ORCHESTRATEUR       │
         │  Lance des sous-agents via Task   │
         └──────────────────────────────────┘
                        │
        ┌───────────────┼────────────────┬──────────────┐
        ↓               ↓                ↓              ↓
    ┌──────┐     ┌─────────────┐    ┌──────┐      ┌──────┐
    │Agent1│     │   PARALLÈLE  │    │Agent4│      │Agent5│
    │Setup │     │ Agent2 Agent3│    │Pages │      │Content│
    │      │     │ Comp.  Sect. │    │      │      │       │
    └──────┘     └─────────────┘    └──────┘      └──────┘
     0-8%         8-24% simultané    24-32%        32-40%
```

### Fonctionnement:
1. Agent Orchestrateur utilise **Task tool**
2. Lance Agent1 (Setup) → attend fin
3. Lance **EN PARALLÈLE** Agent2 (Components) + Agent3 (Sections)
4. Attend que les 2 terminent
5. Lance Agent4 (Pages) qui utilise le travail de 2+3
6. Lance Agent5 (Content)

### Caractéristiques:
- ✅ **RAPIDE** (parallélisme Phases 2+3)
- ✅ Agents **AUTONOMES** (contexte isolé)
- ✅ **Résilient** (un agent peut échouer sans tout casser)
- ✅ **Scalable** (peut lancer plus d'agents si besoin)
- ⚠️ Plus complexe à orchestrer
- ⚠️ Nécessite Claude Code SDK avec Task tool

---

## 📊 Comparaison Performance

| Aspect | Modulaire Séquentiel | Multi-Agents Parallèle |
|--------|---------------------|----------------------|
| **Temps Phase 1** | 2 min | 2 min |
| **Temps Phases 2+3** | 4 min (2+2) | **2 min** (parallèle ⚡) |
| **Temps Phase 4** | 2 min | 2 min |
| **Temps Phase 5** | 1 min | 1 min |
| **TOTAL** | **9 minutes** | **7 minutes** (-22%) |
| **Agents Claude** | 1 (réutilisé) | 5 (autonomes) |
| **Coût tokens** | Moyen | Légèrement supérieur |

---

## 🎯 Quand utiliser quoi?

### Utiliser **Modulaire Séquentiel** si:
- Débogage nécessaire (plus simple à tracer)
- Budget tokens serré
- Phases fortement dépendantes
- Simplicité > Performance

### Utiliser **Multi-Agents Parallèle** si:
- Performance critique
- Phases indépendantes
- Beaucoup de sites à générer en parallèle
- Veux vrais agents autonomes

---

## 💡 Architecture Hybride Possible

```
Phase 1: Setup (séquentiel)
    ↓
Phases 2+3: Multi-agents PARALLÈLE (Components + Sections)
    ↓
Phase 4: Pages (séquentiel, utilise 2+3)
    ↓
Phase 5: Content (séquentiel)
```

**Gain: 22% plus rapide sans complexité excessive**

---

## 🚀 Pour activer Multi-Agents

Dans `app/api/routers.py`:

```python
# Ancien (séquentiel)
from app.services.generator_modular import GeneratorServiceModular as GeneratorService

# Nouveau (multi-agents)
from app.services.generator_multiagent import GeneratorServiceMultiAgent as GeneratorService
```

Ou créer un paramètre de configuration:

```python
# .env
USE_MULTIAGENT=true

# config.py
use_multiagent: bool = Field(default=False, env="USE_MULTIAGENT")
```
