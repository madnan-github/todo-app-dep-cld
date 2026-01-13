import React, { useState, useEffect } from 'react';
import ChatKitWrapper from './components/ChatKitWrapper';

const App: React.FC = () => {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    // Initialize user session or authentication
    // This would typically connect to your auth provider
    console.log('Initializing user session...');
  }, []);

  return (
    <div className="App">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-xl font-bold">Todo AI Chatbot</h1>
      </header>
      <main className="container mx-auto p-4">
        <ChatKitWrapper />
      </main>
    </div>
  );
};

export default App;