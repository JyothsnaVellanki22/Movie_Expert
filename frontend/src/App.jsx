import { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Greetings, I am the Star Wars RAG Bot. Ask me anything about the original trilogy scripts! The Force is strong with this one.",
      sender: "bot"
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMsg = {
      id: Date.now(),
      text: inputValue.trim(),
      sender: "user"
    };

    setMessages(prev => [...prev, userMsg]);
    setInputValue("");
    setIsTyping(true);

    try {
      // Connect to the Python FastAPI backend
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMsg.text })
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      const botMsg = {
        id: Date.now() + 1,
        text: data.response,
        sender: "bot"
      };

      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error("Chat Error:", error);
      const errorMsg = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting to the Force (or the backend server). Please make sure the API is running on port 8000.",
        sender: "bot"
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="app-container">
      <header className="chat-header">
        <h1>
          RAG Bot <span className="status-dot"></span>
        </h1>
        <div style={{ color: "var(--color-text-muted)", fontSize: "0.85rem" }}>
          Star Wars Trilogy Knowledge Base
        </div>
      </header>

      <div className="chat-history">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
            <span className="message-author">
              {msg.sender === 'user' ? 'GUEST' : 'SYSTEM'}
            </span>
            <div className="message-bubble">
              {msg.text}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="message-wrapper bot">
            <span className="message-author">SYSTEM</span>
            <div className="typing-indicator">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-container" onSubmit={handleSend}>
        <input
          type="text"
          className="chat-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask about A New Hope, Empire Strikes Back, or Return of the Jedi..."
          disabled={isTyping}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={!inputValue.trim() || isTyping}
          aria-label="Send Message"
        >
          <svg className="send-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </form>
    </div>
  );
}

export default App;
