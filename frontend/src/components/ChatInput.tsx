import { useState, useEffect, useRef } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import styles from "./ChatInput.module.css";

/**
 * Props for the ChatInput component.
 */
interface ChatInputProps {
  /**
   * Callback function invoked when the user submits a message.
   * Receives the trimmed message text as a parameter. The parent component
   * should handle sending this message to the backend API and updating
   * the conversation state.
   */
  onSendMessage: (message: string) => void;

  /**
   * Whether the input should be disabled (e.g., while waiting for an API response).
   * When true, the textarea and send button are disabled to prevent multiple
   * concurrent submissions. Defaults to false.
   */
  disabled?: boolean;

  /**
   * Optional external value to control the input field.
   * When provided, the component operates in controlled mode, allowing the parent
   * to programmatically set the input value (e.g., when clicking sample questions).
   * If omitted, the component uses internal state (uncontrolled mode).
   */
  value?: string;

  /**
   * Optional callback invoked when the input value changes.
   * Required when using the `value` prop for controlled mode. This allows the parent
   * component to track and update the input state. If omitted while `value` is provided,
   * the input will be read-only.
   */
  onChange?: (value: string) => void;
}

/**
 * Auto-expanding textarea input component for chat messages with smart submit handling.
 *
 * This component provides a sophisticated chat input experience with the following features:
 * - Auto-expanding textarea that grows as the user types (up to 200px max height)
 * - Supports both controlled and uncontrolled modes via optional value/onChange props
 * - Smart keyboard shortcuts: Enter to send, Shift+Enter for new lines
 * - Visual feedback with disabled states during message processing
 * - Clean, accessible UI with proper ARIA labels and form semantics
 *
 * The component can operate in two modes:
 * 1. **Uncontrolled mode** (default): Manages its own state internally
 * 2. **Controlled mode**: When `value` and `onChange` are provided, the parent controls the state
 *
 * The auto-resize feature ensures the textarea expands to show all content while
 * limiting maximum height to maintain a clean UI. The component handles the complexity
 * of synchronizing internal and external state seamlessly.
 *
 * @param props - Component props
 * @param props.onSendMessage - Callback to invoke when a message is submitted (via Enter or button click)
 * @param props.disabled - Whether the input is disabled during API calls (default: false)
 * @param props.value - Optional external value for controlled mode
 * @param props.onChange - Optional change handler for controlled mode
 *
 * @returns A rendered form with auto-expanding textarea and send button
 *
 * @example
 * ```tsx
 * // Uncontrolled mode (component manages its own state)
 * <ChatInput
 *   onSendMessage={(msg) => handleSend(msg)}
 *   disabled={isLoading}
 * />
 *
 * // Controlled mode (parent controls the state)
 * const [input, setInput] = useState('');
 * <ChatInput
 *   value={input}
 *   onChange={setInput}
 *   onSendMessage={(msg) => handleSend(msg)}
 *   disabled={isLoading}
 * />
 * ```
 */
export function ChatInput({
  onSendMessage,
  disabled = false,
  value: externalValue,
  onChange: externalOnChange,
}: ChatInputProps) {
  const [internalMessage, setInternalMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Use external value if provided, otherwise use internal state
  const message = externalValue !== undefined ? externalValue : internalMessage;
  const setMessage =
    externalOnChange !== undefined ? externalOnChange : setInternalMessage;

  // Auto-resize textarea
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  };

  // Sync internal state when external value changes
  useEffect(() => {
    if (externalValue !== undefined) {
      setInternalMessage(externalValue);
    }
    adjustTextareaHeight();
  }, [externalValue, message]);

  const handleChange = (value: string) => {
    setMessage(value);
    // Trigger height adjustment on next tick
    setTimeout(adjustTextareaHeight, 0);
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      handleChange("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.inputWrapper}>
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => handleChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about Federal Reserve speeches..."
          className={styles.textarea}
          disabled={disabled}
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
