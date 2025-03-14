import { View } from 'react-native';
import { Button, TextInput } from 'react-native-paper';
import { useState } from 'react';
import { supabase } from '../lib/supabase';
import { styles } from '../styles';

export default function Home() {
  const [content, setContent] = useState('');

  const handleAnalyze = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        alert('Veuillez vous connecter');
        return;
      }

      const { data, error } = await supabase
        .from('analyses')
        .insert([
          {
            user_id: user.id,
            content,
            type: 'summary'
          }
        ])
        .select()
        .single();

      if (error) throw error;
      alert('Analyse créée avec succès !');
    } catch (error) {
      console.error(error);
      alert('Erreur lors de l\'analyse');
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        mode="outlined"
        multiline
        numberOfLines={4}
        value={content}
        onChangeText={setContent}
        placeholder="Entrez votre texte ici..."
        style={styles.input}
      />
      <Button 
        mode="contained" 
        onPress={handleAnalyze}
        style={styles.button}
      >
        Analyser
      </Button>
    </View>
  );
} 