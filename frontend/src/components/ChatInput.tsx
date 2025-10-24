import { useState, useEffect } from 'react';
import type { FormEvent, KeyboardEvent } from 'react';
import styles from './ChatInput.module.css';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  value?: string;
  onChange?: (value: string) => void;
}

export function ChatInput({ onSendMessage, disabled = false, value: externalValue, onChange: externalOnChange }: ChatInputProps) {
  const [internalMessage, setInternalMessage] = useState('');
  
  // Use external value if provided, otherwise use internal state
  const message = externalValue !== undefined ? externalValue : internalMessage;
  const setMessage = externalOnChange !== undefined ? externalOnChange : setInternalMessage;

  // Sync internal state when external value changes
  useEffect(() => {
    if (externalValue !== undefined) {
      setInternalMessage(externalValue);
    }
  }, [externalValue]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.inputWrapper}>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about Federal Reserve speeches..."
          className={styles.textarea}
          disabled={disabled}
          rows={1}
        />
        <button
          type="submit"
          disabled={!message.trim() || disabled}
          className={styles.sendButton}
          aria-label="Send message"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </form>
  );
}
