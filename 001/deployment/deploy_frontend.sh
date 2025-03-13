#!/bin/bash
echo "Déploiement du frontend..."
cd ../frontend
expo build:android
expo build:ios 