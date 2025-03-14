import { useState } from 'react';
import { View } from 'react-native';
import { TextInput, Button, HelperText } from 'react-native-paper';
import { useFormValidation } from '../hooks/useFormValidation';
import { analysisSchema } from '../validations/schemas';
import { AnalysisService } from '../services/analysis';
import { styles } from '../styles';

export function AnalysisForm() {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const { errors, validate } = useFormValidation(analysisSchema);

  const handleSubmit = async () => {
    const data = { content, type: 'summary' as const };
    
    if (!validate(data)) {
      return;
    }

    try {
      setLoading(true);
      const result = await AnalysisService.analyze(content, 'summary');
      // Traiter le résultat
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
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
        placeholder="Entrez votre texte..."
        error={!!errors.content}
      />
      <HelperText type="error" visible={!!errors.content}>
        {errors.content}
      </HelperText>
      
      <Button 
        mode="contained"
        onPress={handleSubmit}
        loading={loading}
        disabled={loading}
      >
        Analyser
      </Button>
    </View>
  );
} 