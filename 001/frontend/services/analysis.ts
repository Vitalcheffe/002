import { supabase } from '../lib/supabase';
import { Analysis } from '../types/supabase';
import AsyncStorage from '@react-native-async-storage/async-storage';

export class AnalysisService {
  private static CACHE_PREFIX = 'analysis_';
  private static CACHE_DURATION = 1000 * 60 * 60; // 1 heure

  static async analyze(content: string, type: string) {
    try {
      // Vérifier le cache
      const cacheKey = `${this.CACHE_PREFIX}${content}_${type}`;
      const cachedResult = await this.getFromCache(cacheKey);
      if (cachedResult) return cachedResult;

      // Appeler l'API si pas en cache
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Non authentifié');

      const { data, error } = await supabase
        .from('analyses')
        .insert([{ user_id: user.id, content, type }])
        .select()
        .single();

      if (error) throw error;

      // Mettre en cache
      await this.setInCache(cacheKey, data);
      return data;
    } catch (error) {
      console.error('Erreur analyse:', error);
      throw error;
    }
  }

  private static async getFromCache(key: string) {
    try {
      const cached = await AsyncStorage.getItem(key);
      if (!cached) return null;

      const { value, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp > this.CACHE_DURATION) {
        await AsyncStorage.removeItem(key);
        return null;
      }

      return value;
    } catch {
      return null;
    }
  }

  private static async setInCache(key: string, value: any) {
    try {
      await AsyncStorage.setItem(key, JSON.stringify({
        value,
        timestamp: Date.now()
      }));
    } catch (error) {
      console.error('Erreur cache:', error);
    }
  }

  async updateAnalysisResult(id: string, result: any): Promise<Analysis> {
    const { data, error } = await supabase
      .from('analyses')
      .update({
        result,
        status: 'completed'
      })
      .eq('id', id)
      .select()
      .single();

    if (error) throw error;
    return data;
  },

  async getUserAnalyses(userId: string): Promise<Analysis[]> {
    const { data, error } = await supabase
      .from('analyses')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data;
  },

  async getAnalysis(id: string): Promise<Analysis> {
    const { data, error } = await supabase
      .from('analyses')
      .select('*')
      .eq('id', id)
      .single();

    if (error) throw error;
    return data;
  }
} 