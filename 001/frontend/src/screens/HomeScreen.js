import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet } from 'react-native';
import { analyzeContent } from '../api';

export default function HomeScreen({ navigation }) {
  const [content, setContent] = useState('');

  return (
    <View style={styles.container}>
      <TextInput
        multiline
        placeholder="Entrez votre texte ici..."
        value={content}
        onChangeText={setContent}
        style={styles.input}
      />
      <Button title="Générer un résumé" onPress={() => {/* ... */}} />
      <Button title="Créer un quiz" onPress={() => {/* ... */}} />
      <Button title="Générer une carte mentale" onPress={() => {/* ... */}} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  input: {
    height: 200,
    borderWidth: 1,
    padding: 10,
    marginBottom: 20,
  },
}); 