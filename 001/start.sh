#!/bin/bash

# Vérification de l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python -m venv venv
fi

# Activation de l'environnement virtuel
source venv/bin/activate

# Installation des dépendances
pip install -r backend/requirements.txt

# Démarrage de l'application
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 