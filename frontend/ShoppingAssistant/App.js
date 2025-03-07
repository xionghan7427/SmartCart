// App.js
import React, { useState, useEffect } from 'react';
import { SafeAreaView, TextInput, Button, Text, View, ScrollView, StyleSheet, Linking } from 'react-native';
import Voice from '@react-native-community/voice';

const App = () => {
    const [input, setInput] = useState('');
    const [deals, setDeals] = useState([]);
    const [isListening, setIsListening] = useState(false);

    useEffect(() => {
        Voice.onSpeechStart = onSpeechStart;
        Voice.onSpeechRecognized = onSpeechRecognized;
        Voice.onSpeechEnd = onSpeechEnd;
        Voice.onSpeechResults = onSpeechResults;
        Voice.onSpeechError = onSpeechError;

        return () => {
            Voice.destroy().then(Voice.removeAllListeners);
        };
    }, []);

    const onSpeechStart = () => {
        console.log('Speech recognition started');
        setIsListening(true);
    };

    const onSpeechRecognized = () => {
        console.log('Speech recognized');
    };

    const onSpeechEnd = () => {
        console.log('Speech recognition ended');
        setIsListening(false);
    };

    const onSpeechResults = (event) => {
        const spokenText = event.value[0];
        setInput(spokenText);
    };

    const onSpeechError = (event) => {
        console.error(event);
        setIsListening(false);
    };

    const findDeals = async () => {
        try {
            const response = await fetch('http://YOUR_SERVER_URL/find_deals', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input }),
            });
            const result = await response.json();
            setDeals(result);
        } catch (error) {
            console.error(error);
        }
    };

    const startListening = async () => {
        try {
            await Voice.start('en-US');
        } catch (error) {
            console.error(error);
        }
    };

    const displayResults = () => {
        return deals.map((deal, index) => (
            <View key={index} style={styles.dealContainer}>
                <Text style={styles.dealTitle}>{deal.title}</Text>
                <Text style={styles.dealPrice}>{deal.price}</Text>
                <Text style={styles.dealLink} onPress={() => Linking.openURL(deal.link)}>Link</Text>
            </View>
        ));
    };

    const handleStop = () => {
        console.log('Stopping Voice, Voice module:', Voice);
        Voice.stop;
        setIsListening(false);
      };    

    return (
        <SafeAreaView style={styles.container}>
            <Text style={styles.title}>Shopping Assistant</Text>
            <TextInput
                style={styles.input}
                placeholder="Enter your query here"
                value={input}
                onChangeText={setInput}
            />
            <Button title="Find Deals" onPress={findDeals} />
            <Button title={isListening ? "Stop Listening" : "Voice Input"} onPress={isListening ? handleStop : startListening} />
            <ScrollView style={styles.results}>
                {displayResults()}
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 16,
    },
    input: {
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 4,
        padding: 8,
        marginBottom: 16,
    },
    results: {
        marginTop: 16,
    },
    dealContainer: {
        padding: 8,
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
    },
    dealTitle: {
        fontWeight: 'bold',
    },
    dealPrice: {
        color: 'green',
    },
    dealLink: {
        color: 'blue',
        textDecorationLine: 'underline',
    },
});

export default App;
