import { useState, useEffect } from 'react';
import { View, ScrollView } from 'react-native';
import { TextInput, Button, Card, Text } from 'react-native-paper';
import { useSupabase } from '../lib/supabase';
import { analysisService } from '../services/analysis';
import { DeepSeekService } from '../services/deepseek';
import { styles } from '../styles';
import { authService } from '../services/auth';
import { Analysis } from '../types/supabase';

export default function Home() {
  const { supabase } = useSupabase();
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    loadAnalyses();
  }, []);

  const loadAnalyses = async () => {
    try {
      const user = await authService.getCurrentUser();
      if (user) {
        const userAnalyses = await analysisService.getUserAnalyses(user.id);
        setAnalyses(userAnalyses);
      }
    } catch (error) {
      console.error('Erreur chargement analyses:', error);
    }
  };

  const handleAnalyze = async () => {
    try {
      const user = await authService.getCurrentUser();
      if (!user) throw new Error('Non connecté');

      const analysis = await analysisService.createAnalysis(
        user.id,
        content,
        'summary'
      );

      // Simuler l'analyse IA
      const result = { summary: "Résumé test" };
      
      await analysisService.updateAnalysisResult(analysis.id, result);
      await loadAnalyses();
    } catch (error) {
      console.error('Erreur analyse:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <TextInput
        mode="outlined"
        multiline
        numberOfLines={6}
        value={content}
        onChangeText={setContent}
        placeholder="Entrez votre texte à analyser..."
      />
      <Button
        mode="contained"
        onPress={handleAnalyze}
        loading={loading}
        style={styles.button}
      >
        Analyser
      </Button>

      {analyses.map(analysis => (
        <Text key={analysis.id}>
          {analysis.content.substring(0, 50)}...
        </Text>
      ))}

      {result && (
        <Card style={styles.resultCard}>
          <Card.Content>
            <Text variant="titleLarge">Résultat</Text>
            <Text>{result.summary}</Text>
          </Card.Content>
        </Card>
      )}
    </ScrollView>
  );
} 