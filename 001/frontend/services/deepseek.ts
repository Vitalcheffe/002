import Constants from 'expo-constants';

const DEEPSEEK_API_KEY = Constants.expoConfig?.extra?.deepseekApiKey || '';

export class DeepSeekService {
  static async analyze(content: string, type: 'summary' | 'quiz' | 'mindmap') {
    try {
      const response = await fetch('https://api.deepseek.com/v1/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
        },
        body: JSON.stringify({ content, type }),
      });

      if (!response.ok) {
        throw new Error('Erreur analyse DeepSeek');
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur DeepSeek:', error);
      throw error;
    }
  }
} 