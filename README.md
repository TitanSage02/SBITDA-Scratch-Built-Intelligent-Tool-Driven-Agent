# Scratch-Built Intelligent Tool-Driven Agent

**Description :**
Un agent conversationnel intelligent construit de zéro avec une gestion d'outils, des prompts dynamiques et une gestion des réponses de LLM (Large Language Models).

## Architecture :
Le projet est structuré en différents modules :

- `core/`: Contient l'agent principal.
- `controllers/`: Gère les boucles de vérification et les erreurs.
- `managers/`: Gère les prompts, les outils et les réponses.
- `configs/`: Contient les configurations de template de prompt.
- `utils/`: Fonctions utilitaires.

## Fonctionnalités :
- Supporte plusieurs outils externes intégrés.
- Prompt adaptable et dynamique pour générer des interactions efficaces.
- Exécution des actions avec une gestion d'erreurs robuste.

## Installation :
Clonez le repository et installez les dépendances :
```bash
git clone https://github.com/TitanSage02/scratch-built-intelligent-agent.git
cd scratch-built-intelligent-agent
pip install -r requirements.txt
