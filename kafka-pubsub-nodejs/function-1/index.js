// This function receives a message from the Kafka trigger, processes it and sends it to another Kafka topic.
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
    clientId: 'function1-producer',
    brokers: [process.env.KAFKA_BOOTSTRAP_SERVER],
    ssl: false, // Set to true if your Kafka cluster requires SSL
    sasl: {
        mechanism: 'plain',
        username: process.env.KAFKA_USERNAME, // Your Kafka username stored in an environment variable
        password: process.env.KAFKA_PASSWORD // Store password in environment variable
    }
});

exports.handler = async function handler(event, context) {
    const topicName = 'topic-b';

    console.log(`received new request, request id: %s`, context.requestId);
    console.log(`event: `, event);
    const message = event.data;

    // Simple processing: append a processedAt timestamp
    message.processedAt = new Date().toISOString();

    const producer = kafka.producer();
    await producer.connect();
    await producer.send({
        topic: topicName,
        messages: [{ value: JSON.stringify(message) }],
    });
    await producer.disconnect();

    console.log(`Successfully processed and sent this message to ${topicName}: "${JSON.stringify(message)}"`);

    return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'message': `message received and processed: ${JSON.stringify(message)}` }),
    };
};
