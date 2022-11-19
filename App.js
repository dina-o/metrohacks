import * as React from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Image, View } from 'react-native';
import { Button, Provider as PaperProvider, Text, TextInput } from 'react-native-paper';



export default function App() {

  return (
      <Image source={require('./assets/full-logo.png')} style={styles.logo} />
  );
}


const styles = StyleSheet.create({

});