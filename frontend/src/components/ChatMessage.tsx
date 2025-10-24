import type { ChatMessage } from "../types";
import { User, Bot } from "lucide-react";
import styles from "./ChatMessage.module.css";

/**
 * Props for the ChatMessageComponent.
 */
interface ChatMessageProps {
  /**
   * The message object to render, containing the message content, role (user/assistant),
   * optional sources, and metadata. The component renders differently based on whether
   * the message is from the user or the AI assistant.
   */
  message: ChatMessage;
}

/**
 * Displays a single chat message with role-appropriate styling and optional source citations.
 *
 * This component renders individual messages in the chat conversation, with distinct
 * visual styling for user messages (right-aligned) and assistant messages (left-aligned).
 * For assistant messages, it also displays source citations when available, allowing
 * users to verify the information and explore the original Federal Reserve speeches.
 *
 * Visual features:
 * - User messages: Right-aligned with user icon, simpler styling
 * - Assistant messages: Left-aligned with bot icon, includes sources section
 * - Sources are rendered as clickable links that open in new tabs
 * - Responsive design adapts to different screen sizes
 *
 * @param props - Component props
 * @param props.message - The ChatMessage object containing content, role, and optional sources
 *
 * @returns A rendered message bubble with appropriate styling and content
 *
 * @example
 * ```tsx
 * const userMessage: ChatMessage = {
 *   id: '1',
 *   role: 'user',
 *   content: 'What is inflation?',
 *   timestamp: new Date()
 * };
 *
 * const assistantMessage: ChatMessage = {
 *   id: '2',
 *   role: 'assistant',
 *   content: 'Inflation is the rate at which prices increase...',
 *   sources: ['https://example.com/speech1', 'https://example.com/speech2'],
 *   timestamp: new Date()
 * };
 *
 * <ChatMessageComponent message={userMessage} />
 * <ChatMessageComponent message={assistantMessage} />
 * ```
 */
export function ChatMessageComponent({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`${styles.messageWrapper} ${isUser ? styles.user : styles.assistant}`}
    >
      <div className={styles.message}>
        {!isUser && (
          <div className={styles.avatar}>
            <Bot size={20} />
          </div>
        )}
        <div className={styles.content}>
          <div className={styles.text}>{message.content}</div>

          {!isUser && message.sources && message.sources.length > 0 && (
            <>
              <hr className={styles.divider} />
              <div className={styles.sources}>
                <h4 className={styles.sourcesTitle}>Sources</h4>
                <ul className={styles.sourcesList}>
                  {message.sources.map((source, index) => (
                    <li key={index}>
                      <a
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={styles.sourceLink}
                      >
                        {source}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>
        {isUser && (
          <div className={styles.avatar}>
            <User size={20} />
          </div>
        )}
      </div>
    </div>
  );
}
