export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp: Date;
}

export interface AgentResponse {
  answer: string;
  sources: string[];
}

export interface ChatRequest {
  message: string;
}
