# Guide de Migration vers l'Architecture Modulaire

## 📋 État actuel

✅ **COMPLÉTÉ** :
- Phase 1: Setup Agent créé (`app/agents/modular/phase1_setup.py`)
- Phase 2: Components Agent créé (`app/agents/modular/phase2_components.py`)
- Phase 3: Sections Agent créé (`app/agents/modular/phase3_sections.py`)
- Phase 4: Pages Agent créé (`app/agents/modular/phase4_pages.py`)
- Phase 5: Content Agent créé (`app/agents/modular/phase5_content.py`)
- `__init__.py` créé pour exports
- `GeneratorServiceModular` créé (`app/services/generator_modular.py`)

⏳ **À FAIRE** :
- Tester localement
- Basculer l'API
- Déployer sur le serveur

## 🔄 Option 1: Migration Douce (Recommandée)

### Étape 1: Activer le mode modulaire par défaut

Modifier `app/api/routers.py` ligne 18:

**AVANT:**
```python
from app.services.generator import GeneratorService
```

**APRÈS:**
```python
# Ancien système monolithique (disponible si besoin)
# from app.services.generator import GeneratorService

# Nouveau système modulaire (5 phases)
from app.services.generator_modular import GeneratorServiceModular as GeneratorService
```

### Étape 2: Aucune autre modification nécessaire

Le reste du code fonctionne tel quel car on a renommé la classe avec `as GeneratorService`.

### Étape 3: Déployer

```bash
# Sur votre machine locale, pousser les changements
git add .
git commit -m "Implement modular 5-phase generation architecture"
git push origin main

# Sur le serveur
ssh root@138.197.72.236
cd /root/saasagent
git pull
systemctl restart saas-generator
```

## 🧪 Option 2: Test Parallèle (Plus Prudent)

### Étape 1: Ajouter un endpoint de test

Ajouter dans `app/api/routers.py`:

```python
from app.services.generator_modular import GeneratorServiceModular

@router.post("/generate-v2")  # Nouveau endpoint
async def generate_site_v2(request: SiteGenerationRequest, background_tasks: BackgroundTasks):
    """
    Génération de site avec architecture modulaire (5 phases)
    Version de test - utilise GeneratorServiceModular
    """
    site_slug = f"{request.name.lower().replace(' ', '-')}-{request.city.lower()}"
    job_id = job_manager.create_job(site_slug)

    business_dict = request.model_dump()
    background_tasks.add_task(
        GeneratorServiceModular.run_generation_workflow,  # Version modulaire
        job_id,
        business_dict,
        site_slug
    )

    return JobResponse(
        job_id=job_id,
        status="pending",
        message="Génération démarrée avec architecture modulaire (5 phases)"
    )
```

### Étape 2: Tester

```bash
# Tester l'ancien endpoint (monolithique)
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d @test_payload.json

# Tester le nouveau endpoint (modulaire)
curl -X POST http://localhost:8000/api/generate-v2 \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

### Étape 3: Comparer les résultats

- Les deux jobs devraient produire un site similaire
- Version modulaire devrait avoir des logs plus clairs (Phase 1/5, Phase 2/5, etc.)
- Version modulaire devrait avoir meilleur suivi de progression

### Étape 4: Basculer en production

Une fois validé, remplacer `/generate` par la version modulaire (voir Option 1).

## 📊 Vérifications

### Logs attendus - Version Modulaire

```
2025-01-03 10:00:00 - INFO - 🔨 Phase 1/5: Setup en cours...
2025-01-03 10:01:00 - INFO - ✅ Phase 1/5: Setup terminée
2025-01-03 10:01:01 - INFO - 🔨 Phase 2/5: Components UI en cours...
2025-01-03 10:02:00 - INFO - ✅ Phase 2/5: Components UI terminée
2025-01-03 10:02:01 - INFO - 🔨 Phase 3/5: Sections en cours...
2025-01-03 10:03:00 - INFO - ✅ Phase 3/5: Sections terminée
2025-01-03 10:03:01 - INFO - 🔨 Phase 4/5: Pages & Layout en cours...
2025-01-03 10:04:00 - INFO - ✅ Phase 4/5: Pages & Layout terminée
2025-01-03 10:04:01 - INFO - 🔨 Phase 5/5: SEO & Content en cours...
2025-01-03 10:05:00 - INFO - ✅ Phase 5/5: SEO & Content terminée
2025-01-03 10:05:01 - INFO - 🔍 Phase 6: Validation qualité (tentative 1/3)...
...
```

### Fichiers attendus

Après génération complète, vérifier que le site contient:

```
generated-sites/
└── nom-entreprise-ville/
    ├── package.json                     # Phase 1
    ├── tailwind.config.js               # Phase 1
    ├── next.config.mjs                  # Phase 1
    ├── tsconfig.json                    # Phase 1
    ├── app/
    │   ├── globals.css                  # Phase 1
    │   ├── layout.tsx                   # Phase 4 + Phase 5 (metadata)
    │   ├── page.tsx                     # Phase 4
    │   ├── (pages)/
    │   │   ├── mentions-legales/        # Phase 4
    │   │   └── politique-confidentialite/ # Phase 4
    │   └── api/
    │       └── contact/
    │           └── route.ts             # Phase 5
    ├── components/
    │   ├── ui/                          # Phase 2
    │   │   ├── Button.tsx
    │   │   ├── Input.tsx
    │   │   ├── Card.tsx
    │   │   ├── Accordion.tsx
    │   │   ├── Tabs.tsx
    │   │   └── index.ts
    │   ├── sections/                    # Phase 3
    │   │   ├── Hero.tsx
    │   │   ├── Stats.tsx
    │   │   ├── Services.tsx
    │   │   ├── Testimonials.tsx
    │   │   ├── FAQ.tsx
    │   │   ├── FinalCTA.tsx
    │   │   └── index.ts
    │   ├── layout/                      # Phase 4
    │   │   ├── Header.tsx
    │   │   ├── Footer.tsx
    │   │   └── index.ts
    │   ├── forms/                       # Phase 4
    │   │   ├── ContactForm.tsx
    │   │   └── index.ts
    │   └── seo/                         # Phase 5
    │       ├── StructuredData.tsx
    │       └── index.ts
    ├── lib/
    │   └── utils.ts                     # Phase 2
    ├── public/
    │   ├── sitemap.xml                  # Phase 5
    │   ├── robots.txt                   # Phase 5
    │   └── manifest.json                # Phase 5
    ├── node_modules/                    # Phase 1 (npm install)
    └── README.md                        # Phase 5
```

## 🔍 Tests de validation

### Test 1: Génération complète

```bash
# Lancer génération
curl -X POST http://localhost:8000/api/generate-v2 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Plomberie",
    "location": "Luxembourg",
    "phone": "661234567",
    "email": "test@plomberie.lu",
    "year": 2020,
    "services": "Dépannage, Installation, Réparation",
    "positioning": "Expert en plomberie",
    "street": "1 rue Test",
    "postal_code": "L-1234",
    "city": "Luxembourg"
  }'

# Noter le job_id retourné
```

### Test 2: Vérifier progression

```bash
# Remplacer JOB_ID par la valeur retournée
curl http://localhost:8000/api/status/JOB_ID

# Devrait montrer:
# - progress: 8 après Phase 1
# - progress: 16 après Phase 2
# - progress: 24 après Phase 3
# - progress: 32 après Phase 4
# - progress: 40 après Phase 5
# - progress: 58 après Validation
# - progress: 75 après GitHub
# - progress: 100 après Vercel
```

### Test 3: Build local

```bash
cd /tmp/generated-sites/test-plomberie-luxembourg
npm run build

# Devrait compiler sans erreurs TypeScript
# Devrait générer .next/ correctement
```

### Test 4: Dev local

```bash
npm run dev
# Ouvrir http://localhost:3000
# Vérifier:
# - Header responsive
# - Hero section
# - Stats animés
# - Services grid
# - Testimonials
# - FAQ accordion
# - Contact form multi-étapes
# - Footer
```

## ⚡ Avantages de la version modulaire

### Logs plus clairs
**Avant (monolithique):**
```
Phase 1/4: Génération du code Next.js complet...
Code généré, build en cours...  (40%)
```

**Après (modulaire):**
```
🔨 Phase 1/5: Setup en cours... (0%)
✅ Phase 1/5: Setup terminée (8%)
🔨 Phase 2/5: Components UI en cours... (8%)
✅ Phase 2/5: Components UI terminée (16%)
...
```

### Meilleure granularité progression
- **Avant**: 0% → 40% (génération complète en un bloc)
- **Après**: 0% → 8% → 16% → 24% → 32% → 40% (5 étapes claires)

### Debug facilité
- Si Phase 3 échoue, on sait exactement que c'est dans la génération des sections
- On peut régénérer JUSTE Phase 3 sans tout refaire

### Extensibilité
- Facile d'ajouter Phase 6: Blog
- Facile d'ajouter Phase 7: E-commerce
- Chaque phase = 1 fichier Python simple

## 🚨 Rollback si besoin

Si la version modulaire pose problème:

```python
# Dans app/api/routers.py, revenir à:
from app.services.generator import GeneratorService
```

L'ancien système reste intact dans `app/services/generator.py`.

## 📝 Checklist de migration

- [ ] Créer tous les fichiers phase*.py (✅ FAIT)
- [ ] Créer generator_modular.py (✅ FAIT)
- [ ] Créer __init__.py dans modular/ (✅ FAIT)
- [ ] Lire ce guide
- [ ] Choisir Option 1 (migration directe) ou Option 2 (test parallèle)
- [ ] Modifier routers.py selon l'option choisie
- [ ] Tester en local avec test_payload.json
- [ ] Vérifier les logs
- [ ] Vérifier les fichiers générés
- [ ] Build le site généré (`npm run build`)
- [ ] Tester le site en dev (`npm run dev`)
- [ ] Commit et push vers GitHub
- [ ] Déployer sur le serveur
- [ ] Redémarrer le service
- [ ] Tester sur le serveur
- [ ] Monitorer les premiers jobs

## 🎉 Conclusion

Architecture modulaire prête à déployer !
- ✅ AUCUN prompt perdu
- ✅ Même ENRICHIS
- ✅ Meilleure maintenabilité
- ✅ Meilleur suivi progression
- ✅ Debug facilité
- ✅ Extensible
