import type { ChatMessage } from '../types';
import { User, Bot } from 'lucide-react';
import styles from './ChatMessage.module.css';

interface ChatMessageProps {
  message: ChatMessage;
}

export function ChatMessageComponent({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`${styles.messageWrapper} ${isUser ? styles.user : styles.assistant}`}>
      <div className={styles.message}>
        {!isUser && (
          <div className={styles.avatar}>
            <Bot size={20} />
          </div>
        )}
        <div className={styles.content}>
          <div className={styles.text}>
            {message.content}
          </div>
          
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
