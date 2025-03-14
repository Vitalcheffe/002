#!/bin/bash
set -e

# Variables
ENVIRONMENT="production"
VERSION=$(git describe --tags)
NAMESPACE="deepstudy-prod"

# Vérifications pré-déploiement
echo "🔍 Vérifications pré-déploiement..."

# Tests
echo "🧪 Exécution des tests..."
python -m pytest --cov=backend tests/

# Build
echo "🏗️ Construction de l'image Docker..."
docker build -t deepstudy-ai:${VERSION} .

# Backup
echo "💾 Création du backup..."
python manage.py create_backup

# Déploiement
echo "🚀 Déploiement en production..."
kubectl apply -f kubernetes/production/

# Mise à jour de l'image
kubectl set image deployment/deepstudy-ai \
    deepstudy-ai=deepstudy-ai:${VERSION} \
    --namespace=${NAMESPACE}

# Vérification
echo "✅ Vérification du déploiement..."
kubectl rollout status deployment/deepstudy-ai \
    --namespace=${NAMESPACE} \
    --timeout=300s

echo "✨ Déploiement terminé avec succès!" 