import Constants from 'expo-constants';

export const ENV = {
  SUPABASE_URL: Constants.expoConfig?.extra?.SUPABASE_URL as string,
  SUPABASE_ANON_KEY: Constants.expoConfig?.extra?.SUPABASE_ANON_KEY as string,
  DEEPSEEK_API_KEY: Constants.expoConfig?.extra?.DEEPSEEK_API_KEY as string,
  API_URL: Constants.expoConfig?.extra?.API_URL as string,
}; 