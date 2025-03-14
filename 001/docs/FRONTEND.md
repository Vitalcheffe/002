# Documentation Frontend Deep Study AI

## Structure du Projet

```typescript
frontend/
├── app/                 # Pages de l'application
├── components/          # Composants réutilisables
├── services/           # Services API et logique métier
├── hooks/              # Hooks personnalisés
├── validations/        # Schémas de validation
└── types/              # Types TypeScript
```

## Configuration

1. Variables d'environnement :
```env
EXPO_PUBLIC_SUPABASE_URL=votre_url
EXPO_PUBLIC_SUPABASE_ANON_KEY=votre_clé
EXPO_PUBLIC_DEEPSEEK_API_KEY=votre_clé_deepseek
```

2. Installation :
```bash
npm install
```

3. Démarrage :
```bash
npx expo start
```

## Validation des Données

Nous utilisons Zod pour la validation des données :

```typescript
import { analysisSchema } from '../validations/schemas';

// Exemple d'utilisation
const { errors, validate } = useFormValidation(analysisSchema);
```

## Cache

Le système de cache utilise AsyncStorage pour stocker les résultats :
- Durée de cache : 1 heure
- Invalidation automatique
- Gestion des erreurs

## Bonnes Pratiques

1. Validation :
   - Toujours valider les entrées utilisateur
   - Utiliser les schémas Zod appropriés

2. Gestion des Erreurs :
   - Capturer et logger toutes les erreurs
   - Afficher des messages utilisateur appropriés

3. Performance :
   - Utiliser le cache quand possible
   - Optimiser les requêtes API 