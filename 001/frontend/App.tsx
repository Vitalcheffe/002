import { Provider as PaperProvider } from 'react-native-paper';
import { Slot } from 'expo-router';
import { SupabaseProvider } from './lib/supabase';
import { theme } from './theme';

export default function App() {
  return (
    <SupabaseProvider>
      <PaperProvider theme={theme}>
        <Slot />
      </PaperProvider>
    </SupabaseProvider>
  );
} 