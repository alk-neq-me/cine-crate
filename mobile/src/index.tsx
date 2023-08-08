import { useQuery } from '@tanstack/react-query';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
// import { signUpGuestUserFn } from './api/auth';
import { useState } from 'react';
import { root } from './api/root';


export default function App() {
  const [text, setText] = useState<string>();

  const query = useQuery({
    queryKey: ["hello"],
    queryFn: root,
    onSuccess: setText
  });

  if (query.isLoading) return <Text>Loading...</Text>

  return (
    <View style={styles.container}>
      <Text>{text}</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
