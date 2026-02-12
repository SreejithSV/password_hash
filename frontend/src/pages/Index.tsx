import { useState, useCallback } from "react";
import Header from "../components/Header";
import ActionButtons from "../components/ActionButtons";
import TerminalConsole from "../components/TerminalConsole";
import PerformanceGraph from "../components/PerformanceGraph";
import Footer from "../components/Footer";

const demoLogs: Record<string, string[]> = {
  "GUI Application": [
    "[INFO] Initializing GUI Application...",
    "[INFO] Loading rainbow table: rt_md5_loweralpha_7.rt (2.4 GB)",
    "[OK] Rainbow table loaded successfully",
    "[INFO] CUDA device detected: NVIDIA RTX 4090",
    "[INFO] Allocating GPU memory: 4096 MB",
    "[OK] GPU memory allocated",
    "[INFO] Starting hash lookup engine...",
    "[OK] GUI Application ready — awaiting input",
    "[SUCCESS] System online. Enter hash to crack.",
  ],
  "Command-Line Demo": [
    "[INFO] === Rainbow Table CLI v2.1.0 ===",
    "[INFO] Loading chain file: md5_chains_8char.bin",
    "[OK] Loaded 847,291,456 chains",
    "[INFO] Target hash: 5d41402abc4b2a76b9719d911017c592",
    "[INFO] Searching chain endpoints...",
    "[INFO] Found 3 candidate chains",
    "[INFO] Regenerating chain #1: start=ax9kL2...",
    "[INFO] Regenerating chain #2: start=mP3qR7...",
    "[SUCCESS] Password found: 'hello'",
    "[INFO] Lookup time: 0.042s (CUDA) vs 3.891s (CPU)",
    "[OK] Speedup: 92.6x",
  ],
  "Quick Test": [
    "[INFO] Quick Test Mode — single hash lookup",
    "[INFO] Hash: e10adc3949ba59abbe56e057f20f883e",
    "[INFO] Algorithm: MD5",
    "[INFO] Searching rainbow table...",
    "[INFO] ██████████████████████████ 100%",
    "[SUCCESS] Cracked! Password: '123456'",
    "[INFO] Time elapsed: 0.018s",
  ],
  "Plot Performance": [
    "[INFO] Benchmarking CUDA vs CPU performance...",
    "[INFO] Test 1/5: 1000 hashes — CUDA: 2ms, CPU: 156ms",
    "[INFO] Test 2/5: 5000 hashes — CUDA: 8ms, CPU: 780ms",
    "[INFO] Test 3/5: 10000 hashes — CUDA: 14ms, CPU: 1420ms",
    "[INFO] Test 4/5: 50000 hashes — CUDA: 52ms, CPU: 7100ms",
    "[INFO] Test 5/5: 100000 hashes — CUDA: 98ms, CPU: 14200ms",
    "[OK] Benchmark complete. Rendering graph...",
    "[SUCCESS] Performance graph updated.",
  ],
};

const perfData = [
  { name: "1K", cuda: 2, cpu: 156 },
  { name: "5K", cuda: 8, cpu: 780 },
  { name: "10K", cuda: 14, cpu: 1420 },
  { name: "50K", cuda: 52, cpu: 7100 },
  { name: "100K", cuda: 98, cpu: 14200 },
];

const Index = () => {
  const [consoleLines, setConsoleLines] = useState<string[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [graphData, setGraphData] = useState<{ name: string; cuda: number; cpu: number }[]>([]);

  const handleAction = useCallback((action: string) => {
    const logs = demoLogs[action] || demoLogs["Quick Test"];
    setConsoleLines([]);
    setIsRunning(true);

    logs.forEach((line, i) => {
      setTimeout(() => {
        setConsoleLines((prev) => [...prev, line]);
        if (i === logs.length - 1) {
          setIsRunning(false);
          if (action === "Plot Performance") {
            setGraphData(perfData);
          }
        }
      }, (i + 1) * 400);
    });
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-background grid-bg relative">
      <div className="scanline-overlay" />
      <Header />
      <main className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 py-8 space-y-8">
        <ActionButtons onAction={handleAction} />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <TerminalConsole lines={consoleLines} isRunning={isRunning} />
          <PerformanceGraph data={graphData} />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Index;
