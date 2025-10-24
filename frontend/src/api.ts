import type { AgentResponse, ChatRequest } from "./types";

/**
 * Base URL for the backend API, configured via environment variables.
 * Defaults to localhost:8000 for local development if VITE_API_URL is not set.
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Sends a chat message to the backend RAG agent and returns the response.
 *
 * This function handles communication with the FastAPI backend, posting user messages
 * to the /chat endpoint and receiving structured responses from the RAG agent.
 * The agent processes queries through a retrieval-augmented generation pipeline,
 * searching Federal Reserve speeches and generating contextual answers.
 *
 * The function includes comprehensive error handling for network failures,
 * API errors, and invalid responses. All errors are thrown with descriptive
 * messages to aid in debugging and user feedback.
 *
 * @param message - The user's question or query to send to the RAG agent.
 *                  Should be a well-formed question about Federal Reserve speeches,
 *                  economic policy, or related topics.
 *
 * @returns A Promise that resolves to an AgentResponse containing:
 *          - answer: The synthesized response from the RAG agent
 *          - sources: Array of citations from the Federal Reserve speech knowledge base
 *
 * @throws {Error} When the API request fails due to:
 *         - Network connectivity issues
 *         - HTTP error status codes (4xx, 5xx)
 *         - Invalid JSON responses
 *         - Backend service unavailability
 *         Error messages include status code and response text for debugging.
 *
 * @example
 * ```typescript
 * try {
 *   const response = await sendChatMessage("What is the Fed's inflation target?");
 *   console.log(response.answer);
 *   console.log(response.sources);
 * } catch (error) {
 *   console.error("Failed to get response:", error);
 * }
 * ```
 */
export async function sendChatMessage(message: string): Promise<AgentResponse> {
  const request: ChatRequest = { message };

  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `API request failed: ${response.status} ${response.statusText} - ${errorText}`,
    );
  }

  return response.json();
}
