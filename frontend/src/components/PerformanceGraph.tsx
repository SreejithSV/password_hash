import { motion } from "framer-motion";
import { BarChart3 } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface PerformanceGraphProps {
  data: { name: string; cuda: number; cpu: number }[];
}

const PerformanceGraph = ({ data }: PerformanceGraphProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.7 }}
    >
      <div className="flex items-center gap-2 mb-3">
        <BarChart3 className="w-4 h-4 neon-text-cyan" />
        <span className="font-display text-xs tracking-[0.2em] uppercase neon-text-cyan">
          Performance Metrics
        </span>
      </div>
      <div className="terminal-box neon-border-cyan rounded-lg p-4 h-72">
        {data.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
            {">"} Run a test to generate performance data...
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} barGap={4}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(180 30% 15%)"
                vertical={false}
              />
              <XAxis
                dataKey="name"
                tick={{ fill: "hsl(180 10% 55%)", fontSize: 11, fontFamily: "JetBrains Mono" }}
                axisLine={{ stroke: "hsl(180 30% 15%)" }}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: "hsl(180 10% 55%)", fontSize: 11, fontFamily: "JetBrains Mono" }}
                axisLine={{ stroke: "hsl(180 30% 15%)" }}
                tickLine={false}
                label={{
                  value: "Time (ms)",
                  angle: -90,
                  position: "insideLeft",
                  fill: "hsl(180 10% 55%)",
                  fontSize: 11,
                  fontFamily: "JetBrains Mono",
                }}
              />
              <Tooltip
                contentStyle={{
                  background: "hsl(240 12% 7%)",
                  border: "1px solid hsl(190 100% 50% / 0.3)",
                  borderRadius: "8px",
                  color: "hsl(180 100% 95%)",
                  fontFamily: "JetBrains Mono",
                  fontSize: 12,
                }}
              />
              <Bar dataKey="cuda" name="CUDA GPU" radius={[4, 4, 0, 0]}>
                {data.map((_, index) => (
                  <Cell key={`cuda-${index}`} fill="hsl(120, 100%, 50%)" fillOpacity={0.8} />
                ))}
              </Bar>
              <Bar dataKey="cpu" name="CPU" radius={[4, 4, 0, 0]}>
                {data.map((_, index) => (
                  <Cell key={`cpu-${index}`} fill="hsl(285, 100%, 50%)" fillOpacity={0.8} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </motion.div>
  );
};

export default PerformanceGraph;
