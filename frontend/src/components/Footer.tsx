import { Github, Shield, Code2 } from "lucide-react";

const Footer = () => {
  return (
    <footer className="py-6 px-6 border-t border-border text-center">
      <div className="flex flex-wrap items-center justify-center gap-6 text-xs text-muted-foreground">
        <div className="flex items-center gap-2">
          <Shield className="w-3.5 h-3.5" />
          <span>Rainbow Table Cracker — FYP 2025</span>
        </div>
        <div className="flex items-center gap-2">
          <Code2 className="w-3.5 h-3.5" />
          <span>CUDA · Python · React</span>
        </div>
        <a
          href="https://github.com"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 transition-colors hover:text-neon-green"
        >
          <Github className="w-3.5 h-3.5" />
          <span>Source Code</span>
        </a>
      </div>
      <div className="mt-3 h-px bg-gradient-to-r from-transparent via-neon-green/20 to-transparent" />
      <p className="mt-3 text-[10px] text-muted-foreground tracking-widest uppercase">
        Built with ♥ for academic research
      </p>
    </footer>
  );
};

export default Footer;
