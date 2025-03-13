# Guide de Déploiement Deep Study AI

## Prérequis
- Docker installé
- kubectl configuré
- Accès GCP configuré
- Domaine configuré

## Étapes de déploiement

1. **Préparation de l'environnement**
```bash
# Configuration des variables d'environnement
cp .env.example .env.production
# Éditer .env.production avec les vraies valeurs

# Configuration de GCP
gcloud auth configure-docker
gcloud container clusters get-credentials deepstudy-cluster
```

2. **Déploiement des secrets**
```bash
# Création des secrets Kubernetes
kubectl create secret generic deepstudy-secrets \
    --from-file=.env.production

# Configuration SSL
kubectl apply -f deployment/kubernetes/production/cert-manager.yml
```

3. **Déploiement de l'application**
```bash
# Déploiement complet
./deployment/deploy.sh production
```

4. **Vérification**
```bash
# Vérifier les pods
kubectl get pods

# Vérifier les services
kubectl get services

# Vérifier les logs
kubectl logs -l app=deepstudy-ai
```

## Monitoring Post-Déploiement

1. Vérifier les métriques dans Grafana
2. Confirmer les alertes dans PagerDuty
3. Vérifier les logs dans CloudWatch 