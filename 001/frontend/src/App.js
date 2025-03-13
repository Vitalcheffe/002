import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { Provider as PaperProvider } from 'react-native-paper';
import { Provider as StoreProvider } from 'react-redux';
import { store } from './store';
import AppNavigator from './navigation/AppNavigator';
import { StripeProvider } from '@stripe/stripe-react-native';

export default function App() {
  return (
    <StoreProvider store={store}>
      <PaperProvider>
        <StripeProvider publishableKey="pk_live_...">
          <NavigationContainer>
            <AppNavigator />
          </NavigationContainer>
        </StripeProvider>
      </PaperProvider>
    </StoreProvider>
  );
} 