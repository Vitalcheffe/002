#!/bin/bash

PREVIOUS_VERSION=$1

if [ -z "$PREVIOUS_VERSION" ]; then
    echo "❌ Spécifiez la version pour le rollback"
    exit 1
fi

echo "⏮️ Rollback vers version $PREVIOUS_VERSION"

# Rollback Kubernetes
kubectl rollout undo deployment/deepstudy-ai --to-revision=$PREVIOUS_VERSION

# Vérification
kubectl rollout status deployment/deepstudy-ai

echo "✅ Rollback terminé" 