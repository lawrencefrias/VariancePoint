"use client";

import { motion } from "framer-motion";
import type { ModuleSummary } from "../lib/types";

const statusColor: Record<ModuleSummary["status"], string> = {
  Green: "bg-emerald-500/20 text-emerald-300",
  Amber: "bg-amber-500/20 text-amber-300",
  Red: "bg-rose-500/20 text-rose-300",
};

export function ModuleCard({ module }: { module: ModuleSummary }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-slate-800 bg-slate-900 p-4"
    >
      <header className="flex items-center justify-between">
        <h3 className="font-medium">{module.name}</h3>
        <span className={`rounded-full px-2 py-0.5 text-xs ${statusColor[module.status]}`}>{module.status}</span>
      </header>
      <p className="mt-3 text-2xl font-semibold">{module.metric}</p>
    </motion.article>
  );
}
