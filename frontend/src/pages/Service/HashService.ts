// HashService.ts
// Service to interact with Rainbow Table Password Cracker API

// Using environment variable for base URL (Vite style)
const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL;

type StreamCallback = (chunk: string) => void;

interface StatusResponse {
  status: string;
  message?: string;
}

/**
 * Launch GUI Application
 * @returns {Promise<StatusResponse>} status message
 */
export async function launchGUI(): Promise<StatusResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/gui`);
    if (!response.ok) throw new Error("Failed to launch GUI");
    return await response.json();
  } catch (error) {
    console.error("launchGUI error:", error);
    throw error;
  }
}

/**
 * Run Command-Line Demo
 * @param {StreamCallback} onData callback to receive streaming output
 */
export async function runDemo(onData: (line: string) => void): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/demo`);
    if (!response.ok) throw new Error("Failed to run demo");

    const reader = response.body?.getReader();
    if (!reader) throw new Error("No response body to read");

    const decoder = new TextDecoder();
    let done = false;

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) onData(decoder.decode(value));
    }
  } catch (error) {
    console.error("runDemo error:", error);
    onData("[ERROR] Failed to fetch demo output");
  }
}


/**
 * Run Quick Test
 * @param {StreamCallback} onData callback to receive streaming output
 */
export async function runTest(onData: StreamCallback): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/test`);
    if (!response.ok) throw new Error("Failed to run test");

    const reader = response.body?.getReader();
    if (!reader) throw new Error("No response body to read");

    const decoder = new TextDecoder();
    let done = false;

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) onData(decoder.decode(value));
    }
  } catch (error) {
    console.error("runTest error:", error);
    throw error;
  }
}

/**
 * Plot Performance Graph
 * @param {number} timeMs CUDA lookup time in milliseconds
 * @param {StreamCallback} onData callback to receive streaming output
 */
export async function plotPerformance(timeMs: number = 2.5, onData: StreamCallback): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/plot?time_ms=${timeMs}`);
    if (!response.ok) throw new Error("Failed to plot performance");

    const reader = response.body?.getReader();
    if (!reader) throw new Error("No response body to read");

    const decoder = new TextDecoder();
    let done = false;

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) onData(decoder.decode(value));
    }
  } catch (error) {
    console.error("plotPerformance error:", error);
    throw error;
  }
}
