import { Chat } from "./components/Chat";

/**
 * Root application component for the AgenticFed chat interface.
 *
 * This component serves as the entry point for the React application,
 * rendering the main Chat component which provides the conversational
 * interface for querying Federal Reserve speeches through the RAG agent.
 *
 * The component structure is intentionally minimal to keep the application
 * architecture simple and maintainable, with all chat functionality
 * encapsulated in the Chat component.
 *
 * @returns The rendered application with the Chat component
 */
function App() {
  return <Chat />;
}

export default App;
