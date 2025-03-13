# Deep Study AI - Backend

## Installation

1. Créer un environnement virtuel :
```python -m venv venv```

2. Activer l'environnement :
- Windows : ```venv\Scripts\activate```
- Unix/MacOS : ```source venv/bin/activate```

3. Installer les dépendances :
```pip install -r requirements.txt```

4. Configurer les variables d'environnement dans `.env`

5. Lancer le serveur :
```uvicorn app:app --reload```

Pour le frontend, ajoutons les écrans et composants manquants :

```javascript:frontend/src/screens/SummaryScreen.js
import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';

export default function SummaryScreen({ route }) {
  const { summary } = route.params;

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Résumé</Text>
      <Text style={styles.content}>{summary}</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  content: {
    fontSize: 16,
    lineHeight: 24,
  },
});
```

```javascript:frontend/src/screens/QuizScreen.js
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function QuizScreen({ route }) {
  const { questions } = route.params;
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);

  return (
    <View style={styles.container}>
      <Text style={styles.question}>{questions[currentQuestion].question}</Text>
      {/* Options de réponse */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  question: {
    fontSize: 20,
    marginBottom: 20,
  },
});
```

```javascript:frontend/src/screens/MindMapScreen.js
import React from 'react';
import { View, StyleSheet } from 'react-native';

export default function MindMapScreen({ route }) {
  const { nodes } = route.params;

  return (
    <View style={styles.container}>
      {/* Implémentation de la carte mentale */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
```

```javascript:frontend/src/screens/SettingsScreen.js
import React from 'react';
import { View, Text, Switch, StyleSheet } from 'react-native';

export default function SettingsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Paramètres</Text>
      {/* Options de paramétrage */}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
}); 