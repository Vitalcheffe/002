#!/bin/bash
set -e

# Configuration
PROJECT_NAME="deepstudy-ai"
ENVIRONMENT=$1 # production ou staging
VERSION=$(git describe --tags)

# Vérification de l'environnement
if [ "$ENVIRONMENT" != "production" ] && [ "$ENVIRONMENT" != "staging" ]; then
    echo "❌ Erreur: Spécifiez l'environnement (production ou staging)"
    exit 1
fi

echo "🚀 Déploiement de $PROJECT_NAME vers $ENVIRONMENT (version $VERSION)"

# 1. Vérifications pré-déploiement
echo "🔍 Vérifications pré-déploiement..."
./deployment/scripts/pre_deploy_checks.sh

# 2. Build des images Docker
echo "🏗️ Construction des images Docker..."
docker build -t $PROJECT_NAME:$VERSION -f deployment/Dockerfile .
docker tag $PROJECT_NAME:$VERSION gcr.io/$PROJECT_NAME/$ENVIRONMENT:$VERSION

# 3. Push vers Google Container Registry
echo "⬆️ Push des images vers GCR..."
docker push gcr.io/$PROJECT_NAME/$ENVIRONMENT:$VERSION

# 4. Déploiement sur Kubernetes
echo "📦 Déploiement sur Kubernetes..."
kubectl apply -f deployment/kubernetes/$ENVIRONMENT/
kubectl set image deployment/$PROJECT_NAME $PROJECT_NAME=gcr.io/$PROJECT_NAME/$ENVIRONMENT:$VERSION

# 5. Vérification du déploiement
echo "✅ Vérification du déploiement..."
kubectl rollout status deployment/$PROJECT_NAME 