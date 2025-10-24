import { useState, useRef, useEffect } from 'react';
import type { ChatMessage } from '../types';
import { sendChatMessage } from '../api';
import { ChatMessageComponent } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { MessageSquare, Bot, Sparkles } from 'lucide-react';
import styles from './Chat.module.css';

const SAMPLE_QUESTIONS = [
  "What are the key themes in recent Federal Reserve speeches?",
  "How has the Fed's stance on inflation evolved over time?",
  "What do Fed officials say about interest rate policy?",
  "Summarize the Fed's views on economic growth and employment"
];

export function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendChatMessage(content);
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuestionClick = (question: string) => {
    setInputValue(question);
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.logoSection}>
            <Sparkles size={28} strokeWidth={2} className={styles.logoIcon} />
            <h1 className={styles.title}>AgenticFed</h1>
          </div>
        </div>
      </header>

      <div className={styles.messagesContainer}>
        <div className={styles.messages}>
          {messages.length === 0 && (
            <div className={styles.emptyState}>
              <div className={styles.introCard}>
                <div className={styles.emptyIcon}>
                  <MessageSquare size={64} strokeWidth={1.5} />
                </div>
                <h2 className={styles.emptyTitle}>Start a conversation</h2>
                <p className={styles.emptyText}>
                  Ask me anything about Federal Reserve speeches
                </p>
                
                <div className={styles.sampleQuestions}>
                  {SAMPLE_QUESTIONS.map((question, index) => (
                    <button
                      key={index}
                      className={styles.questionCard}
                      onClick={() => handleQuestionClick(question)}
                    >
                      <MessageSquare size={16} className={styles.questionIcon} />
                      <span>{question}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <ChatMessageComponent key={message.id} message={message} />
          ))}

          {isLoading && (
            <div className={styles.loadingWrapper}>
              <div className={styles.loadingMessage}>
                <div className={styles.loadingAvatar}>
                  <Bot size={20} />
                </div>
                <div className={styles.loadingContent}>
                  <div className={styles.loadingDots}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className={styles.error}>
              <strong>Error:</strong> {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <ChatInput 
        onSendMessage={handleSendMessage} 
        disabled={isLoading}
        value={inputValue}
        onChange={setInputValue}
      />
    </div>
  );
}
