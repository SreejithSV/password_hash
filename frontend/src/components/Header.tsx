import { motion } from "framer-motion";

import { Shield } from "lucide-react";
import GlitchText from "./GlitchText";

const Header = () => {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="relative py-8 px-6 text-center border-b border-border"
    >
      <div className="flex items-center justify-center gap-3 mb-3">
        <Shield className="w-8 h-8 text-neon-green animate-pulse-glow" />
        <h1 className="text-3xl md:text-5xl font-display font-bold tracking-wider neon-text-green">
          <GlitchText text="RAINBOW TABLE" />
        </h1>
        <Shield className="w-8 h-8 text-neon-green animate-pulse-glow" />
      </div>
      <h2 className="text-lg md:text-xl font-display tracking-[0.3em] uppercase neon-text-cyan">
        Password Cracker
      </h2>
      <p className="mt-2 text-sm text-muted-foreground tracking-widest">
        // Final Year Project — CUDA-Accelerated Hash Lookup
      </p>
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-neon-green/50 to-transparent" />
    </motion.header>
  );
};

export default Header;
