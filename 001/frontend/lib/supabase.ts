import 'react-native-url-polyfill/auto';
import { createClient } from '@supabase/supabase-js';
import { createContext, useContext, useState } from 'react';
import Constants from 'expo-constants';
import { SUPABASE_URL, SUPABASE_API_KEY } from '../env';

export const supabase = createClient(SUPABASE_URL, SUPABASE_API_KEY);

const SupabaseContext = createContext({});

export function SupabaseProvider({ children }) {
  return (
    <SupabaseContext.Provider value={supabase}>
      {children}
    </SupabaseContext.Provider>
  );
}

// Hook personnalisé pour utiliser Supabase
export function useSupabase() {
  return { supabase };
} 