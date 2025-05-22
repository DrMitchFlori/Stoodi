import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';

const TutorChatWorkspacePage = () => {
  const [messages, setMessages] = useState([]);
  const { currentUser } = useAppContext();

  const handleSend = (e) => {
    e.preventDefault();
    const form = e.target;
    const value = form.elements.message.value;
    if (!value) return;
    setMessages([...messages, { sender: currentUser.name, text: value }]);
    form.reset();
  };

  return (
    <div className="p-4 flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex-grow overflow-y-auto space-y-2">
        {messages.map((msg, idx) => (
          <div key={idx} className="bg-gray-100 p-2 rounded">
            <strong>{msg.sender}: </strong>{msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSend} className="mt-2 flex">
        <input name="message" className="flex-grow border rounded-l px-2" placeholder="Say something" />
        <button type="submit" className="bg-primary text-white px-4 rounded-r">Send</button>
      </form>
    </div>
  );
};

export default TutorChatWorkspacePage;
