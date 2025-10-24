import { useState, useRef, useEffect } from "react";
import type { ChatMessage } from "../types";
import { sendChatMessage } from "../api";
import { ChatMessageComponent } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { MessageSquare, Bot, Sparkles } from "lucide-react";
import styles from "./Chat.module.css";

/**
 * Sample questions displayed in the empty state to help users get started.
 * These questions cover common topics in Federal Reserve speeches and demonstrate
 * the types of queries the RAG agent can handle effectively.
 */
const SAMPLE_QUESTIONS = [
  "What are the key themes in recent Federal Reserve speeches?",
  "How has the Fed's stance on inflation evolved over time?",
  "What do Fed officials say about interest rate policy?",
  "Summarize the Fed's views on economic growth and employment",
];

/**
 * Main chat interface component for the AgenticFed application.
 *
 * This component implements a complete conversational interface for querying
 * Federal Reserve speeches through a RAG (Retrieval-Augmented Generation) agent.
 * It manages the full conversation lifecycle including message display, API
 * communication, error handling, and user interactions.
 *
 * Key features:
 * - **Message Management**: Maintains conversation history with both user and assistant messages
 * - **API Integration**: Communicates with the FastAPI backend to send queries and receive responses
 * - **Loading States**: Shows typing indicators while waiting for assistant responses
 * - **Error Handling**: Displays user-friendly error messages when API calls fail
 * - **Empty State**: Shows sample questions to guide first-time users
 * - **Auto-scroll**: Automatically scrolls to the latest message as the conversation grows
 * - **Sample Questions**: Clickable question cards that populate the input field
 *
 * The component uses React hooks for state management:
 * - useState for messages, loading status, errors, and input value
 * - useRef for programmatic scrolling to the latest message
 * - useEffect for auto-scrolling when messages update
 *
 * @returns The rendered chat interface with header, message history, and input area
 *
 * @example
 * ```tsx
 * // Simple usage - the component is self-contained
 * import { Chat } from './components/Chat';
 *
 * function App() {
 *   return <Chat />;
 * }
 * ```
 */
export function Chat() {
  /** Array of all messages in the conversation (both user and assistant) */
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  /** Whether the component is currently waiting for an assistant response */
  const [isLoading, setIsLoading] = useState(false);

  /** Error message to display if API call fails, or null if no error */
  const [error, setError] = useState<string | null>(null);

  /** Current value of the input field, used for controlled input when clicking sample questions */
  const [inputValue, setInputValue] = useState("");

  /** Reference to the scroll target at the end of the message list for auto-scrolling */
  const messagesEndRef = useRef<HTMLDivElement>(null);

  /**
   * Scrolls the message container to show the most recent message.
   * Uses smooth scrolling for a better user experience.
   */
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  /**
   * Handles sending a user message and receiving the assistant's response.
   *
   * This function orchestrates the complete message flow:
   * 1. Creates and adds the user message to the conversation
   * 2. Sets loading state and clears any previous errors
   * 3. Calls the backend API to get the assistant's response
   * 4. Creates and adds the assistant message with sources
   * 5. Handles errors gracefully with user-friendly messages
   *
   * The function manages state transitions carefully to ensure the UI stays
   * in sync with the async API call, including proper cleanup in the finally block.
   *
   * @param content - The user's message text to send to the RAG agent
   */
  const handleSendMessage = async (content: string) => {
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
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
        role: "assistant",
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      console.error("Error sending message:", err);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handles clicking on a sample question card.
   *
   * Populates the input field with the selected question, allowing the user
   * to review or modify it before sending. This provides a better UX than
   * immediately sending the question, giving users control over their queries.
   *
   * @param question - The sample question text to populate in the input field
   */
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
                      <MessageSquare
                        size={16}
                        className={styles.questionIcon}
                      />
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
