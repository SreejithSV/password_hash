import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { TerminalSquare } from "lucide-react";

interface TerminalConsoleProps {
  lines: string[];
  isRunning: boolean;
}

const TerminalConsole = ({ lines, isRunning }: TerminalConsoleProps) => {
  const consoleRef = useRef<HTMLDivElement>(null);
  const [visibleLines, setVisibleLines] = useState<string[]>([]);

  useEffect(() => {
    if (lines.length > visibleLines.length) {
      const timer = setTimeout(() => {
        setVisibleLines(lines.slice(0, visibleLines.length + 1));
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [lines, visibleLines.length]);

  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  }, [visibleLines]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.5 }}
    >
      <div className="flex items-center gap-2 mb-3">
        <TerminalSquare className="w-4 h-4 neon-text-green" />
        <span className="font-display text-xs tracking-[0.2em] uppercase neon-text-green">
          System Output
        </span>
        {isRunning && (
          <span className="ml-auto flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-neon-green animate-pulse-glow" />
            <span className="text-xs text-neon-green">RUNNING</span>
          </span>
        )}
      </div>
      <div
        ref={consoleRef}
        className="terminal-box rounded-lg p-4 h-72 overflow-y-auto font-mono text-sm leading-relaxed"
      >
        {visibleLines.length === 0 ? (
          <span className="text-muted-foreground">
            {">"} Awaiting command...
            <span className="blink-cursor" />
          </span>
        ) : (
          visibleLines.map((line, i) => (
            <div key={i} className="flex">
              <span className="text-muted-foreground mr-2 select-none">
                {String(i + 1).padStart(3, "0")}
              </span>
              <span
                className={
                  line.startsWith("[ERROR]")
                    ? "text-destructive"
                    : line.startsWith("[OK]") || line.startsWith("[SUCCESS]")
                    ? "text-neon-green"
                    : line.startsWith("[INFO]")
                    ? "text-neon-cyan"
                    : "text-terminal-text"
                }
              >
                {line}
              </span>
            </div>
          ))
        )}
        {isRunning && visibleLines.length > 0 && (
          <div className="flex">
            <span className="text-muted-foreground mr-2 select-none">
              {String(visibleLines.length + 1).padStart(3, "0")}
            </span>
            <span className="blink-cursor text-neon-green" />
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default TerminalConsole;
