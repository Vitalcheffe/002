import React from 'react';
import { ActivityIndicator, View, StyleSheet } from 'react-native';

export const LoadingSpinner = ({ size = 'large', color = '#0000ff' }) => (
    <View style={styles.container}>
        <ActivityIndicator size={size} color={color} />
    </View>
);

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
}); 