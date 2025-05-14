// This function is triggered by messages published to the topic 'topic-b' and simply logs the received message.
exports.handler = async function handler(event, context) {
    console.log(`received new request, request id: %s`, context.requestId);
    console.log(`Received message from topic-b: `, event.data);

    return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'message': `received message from topic-b: ${JSON.stringify(event.data)}` }),
    };
};