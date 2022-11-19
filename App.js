import * as React from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Image, View } from 'react-native';
import { Button, Provider as PaperProvider, Text, TextInput } from 'react-native-paper';

export default function App() {
  const [username, setUsername] = React.useState("");
  const [password, setPassword] = React.useState("");

  function loginAttempt() {
    if (username === "sally") {
      setTest("logged in as patient");
    } else {
      setTest("incorrect username/password");
    }
  }

  return (
    <PaperProvider>
      <Image source={require('./assets/full-logo.png')} style={styles.logo} />

      <TextInput
          label="Username"
          value={username}
          onChangeText={username => setUsername(username)}
        />

      <TextInput
          label="Password"
          value={password}
          onChangeText={password => setPassword(password)}
        />

        </PaperProvider>
  );
}

const styles = StyleSheet.create({

});