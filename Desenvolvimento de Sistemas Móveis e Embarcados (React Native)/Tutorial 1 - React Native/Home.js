import * as React from 'react';
import { View, Text, Image, Button, StyleSheet, BackHandler } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <View>
      <View style={styles.container}>
        <Image style={styles.logo} source={require('./assets/snack-icon.png')} />
        <Text style={styles.title} >Tutorial 1</Text>
      </View>
      <View style={styles.button}>
        <Button title="Ver Contatos" onPress={() => navigation.navigate('ContactList')} />
      </View>
      <View style={styles.button}>
        <Button title="Sair" onPress={() => BackHandler.exitApp() } />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 60,
  },
  logo: {
    height: 160,
    width: 160,
  },
  title: {
    padding: 30,
    fontSize: 18,
  },
  button: {
    padding: 15
  }
});