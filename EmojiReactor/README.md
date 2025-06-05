# Discord Image Recognition Bot

Un bot Discord intelligent qui analyse automatiquement les images postées dans un canal spécifique et ajoute des réactions emoji appropriées basées sur le contenu détecté.

## Fonctionnalités

- 🔍 **Reconnaissance d'images** : Utilise l'API OpenAI Vision (GPT-4o) pour analyser les images
- 😊 **Réactions automatiques** : Ajoute des emojis pertinents basés sur le contenu détecté
- 🎯 **Canal ciblé** : Surveille uniquement un canal Discord spécifique
- 📝 **Logs détaillés** : Système de journalisation pour le debugging
- ⚡ **Asynchrone** : Performance optimisée avec traitement asynchrone
- 🛡️ **Gestion d'erreurs** : Robuste avec gestion complète des erreurs

## Formats d'images supportés

- PNG
- JPG/JPEG
- GIF (y compris animé)
- WEBP

## Installation

1. **Cloner le projet**
```bash
git clone <repository-url>
cd discord-image-bot
