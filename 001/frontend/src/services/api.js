import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: process.env.API_URL,
  timeout: 30000,
});

// Intercepteur pour ajouter le token
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Refresh token ou déconnexion
      await handleUnauthorized();
    }
    return Promise.reject(error);
  }
);

export const analyzeContent = async (content, type) => {
  try {
    const response = await api.post('/analyze', { content, type });
    return response.data;
  } catch (error) {
    console.error('Erreur analyse:', error);
    throw error;
  }
}; 