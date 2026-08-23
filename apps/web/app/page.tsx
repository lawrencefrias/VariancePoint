"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { ModuleCard } from "../components/module-card";

const modules = [
  { name: "Technology Mortality Index", metric: "64.2", status: "Amber" as const },
  { name: "Debt Clock", metric: "3 Critical", status: "Red" as const },
  { name: "Variance Engine", metric: "58.0", status: "Amber" as const },
  { name: "Alternate Reality", metric: "3 Branches", status: "Green" as const },
];

const trend = [
  { month: "Jan", drift: 42 },
  { month: "Feb", drift: 45 },
  { month: "Mar", drift: 48 },
  { month: "Apr", drift: 52 },
  { month: "May", drift: 55 },
  { month: "Jun", drift: 58 },
];

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 p-6">
      <section>
        <h1 className="text-3xl font-semibold">VariancePoint</h1>
        <p className="mt-2 text-slate-300">Google Maps for Enterprise Technology Futures.</p>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        {modules.map((module) => (
          <ModuleCard key={module.name} module={module} />
        ))}
      </section>

      <section className="rounded-xl border border-slate-800 bg-slate-900 p-4">
        <h2 className="mb-4 text-xl">Technology Drift Trend</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trend}>
              <XAxis dataKey="month" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Line type="monotone" dataKey="drift" stroke="#38bdf8" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    </main>
  );
}
