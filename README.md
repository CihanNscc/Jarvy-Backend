# Jarvy - AI Assistant - Backend

Jarvy is a dynamic AI assistant powered by OpenAI's GPT-4, integrated with various tools to assist users in multiple domains. The system allows users to interact through text and voice, providing personalized responses based on conversation history, user notes, weather updates, and more. It stores and retrieves conversation data for improved context across interactions.

## Key Features:

**Conversation History:** Jarvy maintains a conversation history stored in MongoDB, allowing for context-aware responses.

**Personalization:** The assistant can fetch user-specific data, including personal details and notes, to tailor responses.

**Weather Information:** Users can request up-to-date weather information based on a fixed location.

**Note Management:** Jarvy can store and retrieve user notes for future reference.

**Text and Voice Interactions:** Users can input queries both via text and voice. Voice inputs are converted to text using speech-to-text technology, and responses are read back using text-to-speech.

**Flask Backend & MongoDB:** The project leverages Flask for the backend, with MongoDB for storing user data and conversation history.

**Real-Time Interaction:** The app offers real-time feedback with a conversational UI built using React, displaying messages and AI responses dynamically.

## Tech Stack:

Flask, MongoDB, OpenAI GPT-4

## Additional Tools:

Audio Recorder, Speech-to-Text, Text-to-Speech, Llama Index for tool management

## Use Case:

Jarvy serves as an intelligent assistant for users who need help organizing their thoughts, managing notes, and staying updated with relevant information like weather. The assistant's ability to recall past conversations and handle real-time interactions makes it an ideal choice for users seeking personalized support.
