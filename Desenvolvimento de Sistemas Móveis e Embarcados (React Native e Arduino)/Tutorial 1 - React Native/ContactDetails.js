import * as React from 'react';
import { Text, View, StyleSheet, Button, Linking } from 'react-native';
import { Platform } from 'react-native';

export default function ContactDetailsScreen({ route, navigation }) {
  const { contact } = route.params;
  const mapUrl = Platform.select({
   ios: 'map',
   android: 'geo'
  });
  return (
    <View>
      <View style={styles.container}>
        <Text style={styles.contactName}>{contact.name}</Text>
        <Text style={styles.contactDetails}>E-mail: {contact.email}</Text>
        <Text style={styles.contactDetails}>Telefone: {contact.phone}</Text>
      </View>
      <View style={styles.button}>
        <Button
          onPress={() => Linking.openURL(`mailto:${contact.email}`)}
          title="Enviar E-mail"
        />
      </View>
      <View style={styles.button}>
        <Button
          onPress={() => Linking.openURL(`tel:${contact.phone}`)}
          title="Ligar"
        />
      </View>
      <View style={styles.button}>
        <Button
          onPress={() => Linking.openURL(`${mapUrl}:${contact.address.geo.lat},${contact.address.geo.lng}?q=${contact.address.geo.lat},${contact.address.geo.lng}`)}
          title="Abrir no Mapa"
        />
      </View>
      <View style={styles.button}>
        <Button
          title="Voltar"
          onPress={() => navigation.navigate('ContactList')}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 15,
  },
  contactName: {
    fontSize: 18,
    fontWeight: 'bold',
    height: 44,
  },
  contactDetails: {
    fontSize: 16,
    height: 44,
  },
  button: {
    padding: 15,
  },
});
