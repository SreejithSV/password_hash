import { motion } from "framer-motion";
import { Monitor, Terminal, Zap, BarChart3 } from "lucide-react";
import type { LucideIcon } from "lucide-react"; 
import { launchGUI, plotPerformance } from "../pages/Service/HashService";
import { toast } from "../components/ui/sonner";
import ToastInput from "../components/ui/ToastInput";
import { useState } from "react";

interface ActionButtonProps {
  icon: LucideIcon;
  label: string;
  description: string;
  variant: "green" | "cyan" | "magenta" | "purple";
  onClick: () => void;
  delay?: number;
}

const variantClass: Record<string, string> = {
  green: "neon-btn",
  cyan: "neon-btn neon-btn-cyan",
  magenta: "neon-btn neon-btn-magenta",
  purple: "neon-btn neon-btn-purple",
};

const textClass: Record<string, string> = {
  green: "neon-text-green",
  cyan: "neon-text-cyan",
  magenta: "neon-text-magenta",
  purple: "text-neon-purple",
};

const ActionButton = ({ icon: Icon, label, description, variant, onClick, delay = 0 }: ActionButtonProps) => (
  <motion.button
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.4, delay }}
    whileHover={{ scale: 1.03 }}
    whileTap={{ scale: 0.97 }}
    onClick={onClick}
    className={`${variantClass[variant]} rounded-lg p-5 text-left w-full group cursor-pointer`}
  >
    <div className="flex items-center gap-3 mb-2">
      <Icon className={`w-5 h-5 ${textClass[variant]} group-hover:animate-pulse-glow`} />
      <span className={`font-display text-sm font-semibold tracking-wider uppercase ${textClass[variant]}`}>
        {label}
      </span>
    </div>
    <p className="text-xs text-muted-foreground leading-relaxed">{description}</p>
  </motion.button>
);

interface ActionButtonsProps {
  onAction: (action: string) => void;
}

const ActionButtons = ({ onAction }: ActionButtonsProps) => {
 const [inputVisible, setInputVisible] = useState(false);
  const [pendingAction, setPendingAction] = useState<string | null>(null);
const handleAction = async (action: string, timeMs: number = 2.5) => {
  try {
    if (action === "GUI Application") {
      const result = await launchGUI();
      toast.success(`GUI launched: ${result.status}`);
      console.log(result);
    }

    if (action === "Plot Performance") {
      // Call the API with the user-specified timeMs
      await plotPerformance(timeMs, (data) => {
        console.log("Streaming output:", data);
        // Optionally display in UI
      });
      toast.success(`Performance plot generated for ${timeMs} ms!`);
    }

  } catch (error) {
    console.error("Action failed:", error);
    toast.error(`Action failed: ${(error as Error).message}`);
  }
};


  const buttons = [
    {
      key: "gui",
      icon: Monitor,
      label: "GUI Application",
      description: "Launch the full graphical interface for hash cracking",
      variant: "green" as const,
    },
    {
      icon: Terminal,
      label: "Command-Line Demo",
      description: "Run the CLI version with real-time output streaming",
      variant: "cyan" as const,
    },
    {
      icon: Zap,
      label: "Quick Test",
      description: "Run a fast hash lookup against the rainbow table",
      variant: "magenta" as const,
    },
    {
      icon: BarChart3,
      label: "Plot Performance",
      description: "Generate CUDA vs CPU performance comparison graphs",
      variant: "purple" as const,
    },
  ];

  return (
      <>
      {inputVisible && pendingAction && (
        <ToastInput
          message="Enter CUDA lookup time in milliseconds:"
          defaultValue="2.5"
          onSubmit={(value) => {
            const timeMs = parseFloat(value) || 2.5;
            handleAction(pendingAction, timeMs);
          }}
          onClose={() => setInputVisible(false)}
        />
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {buttons.map((btn, i) => (
          <ActionButton
            key={btn.label}
            {...btn}
            onClick={() => {
              onAction(btn.label);

              if (btn.label === "Plot Performance") {
                setPendingAction(btn.label);
                setInputVisible(true); // show the input toast
              } else {
                handleAction(btn.label);
              }
            }}
            delay={0.1 * (i + 1)}
          />
        ))}
      </div>
    </>

  );
};

export default ActionButtons;
