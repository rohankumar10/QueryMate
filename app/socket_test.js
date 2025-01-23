// Assuming you're using Socket.IO in a JavaScript environment
const socket = io('http://localhost:5000'); // Make sure the URL matches your Flask app

socket.on('connect', () => {
    console.log('Connected to server');

    // Emit the new_chat event with data
    socket.emit('new_chat', {
    input_question_text: 'Your question here',
    question_id: 'someQuestionId',
    chat_id: 'someChatId',
    user_id: 'someUserId',
    user_alias: 'User Alias',
    user_location: 'User Location',
    start_time: new Date().toISOString(), // or your desired format
    media: 'path/to/media', // if applicable
    media_type: 'image' // or other types if applicable
});

});

// Listen for the assistant_message event
socket.on('assistant_message', (data) => {
    console.log('Received message:', data.message);
});
