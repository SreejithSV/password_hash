import { useEffect, useState } from "react";
import { motion } from "framer-motion";

const glitchChars = "!@#$%^&*()_+-=[]{}|;':\",./<>?";

interface GlitchTextProps {
  text: string;
  className?: string;
}

const GlitchText = ({ text, className = "" }: GlitchTextProps) => {
  const [displayText, setDisplayText] = useState(text);
  const [isGlitching, setIsGlitching] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsGlitching(true);
      let iterations = 0;
      const glitchInterval = setInterval(() => {
        setDisplayText(
          text
            .split("")
            .map((char, i) => {
              if (i < iterations) return text[i];
              if (char === " ") return " ";
              return glitchChars[Math.floor(Math.random() * glitchChars.length)];
            })
            .join("")
        );
        iterations += 1;
        if (iterations > text.length) {
          clearInterval(glitchInterval);
          setDisplayText(text);
          setIsGlitching(false);
        }
      }, 30);
    }, 5000);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <motion.span
      className={`${className} ${isGlitching ? "glitch-text" : ""}`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {displayText}
    </motion.span>
  );
};

export default GlitchText;
