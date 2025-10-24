import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";

/**
 * Application entry point that renders the React app to the DOM.
 *
 * This file initializes the React application by:
 * 1. Finding the root DOM element (#root in index.html)
 * 2. Creating a React root using the modern createRoot API (React 18+)
 * 3. Rendering the App component wrapped in StrictMode
 *
 * StrictMode enables additional development checks and warnings to help
 * identify potential problems in the application, including:
 * - Detecting unsafe lifecycles
 * - Warning about legacy APIs
 * - Detecting unexpected side effects
 *
 * Note: StrictMode only runs in development and has no impact on production builds.
 */
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
