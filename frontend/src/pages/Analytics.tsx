import { useCallback } from "react";
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { EmptyState, ErrorState, LoadingState } from "../components/common/AsyncState";
import { usePolling } from "../hooks/usePolling";
import { getMeasurements, getQueues } from "../services/api";

const colors = ["#10b981", "#f59e0b", "#f97316", "#ef4444", "#64748b"];

export function Analytics() {
  const request = useCallback(async () => {
    const queues = await getQueues();
    const results = await Promise.all(queues.map(async (queue) => ({ queue, measurements: await getMeasurements(queue.id) })));
    return results;
  }, []);
  const { data, error, loading, refresh } = usePolling(request);
  if (loading) return <LoadingState label="Loading analytics…" />;
  if (error || !data) return <ErrorState label={error ?? "Unable to load analytics."} retry={refresh} />;
  if (!data.length) return <EmptyState label="No queues found. Analytics will appear when queues are registered." />;
  const population = data.flatMap(({ queue, measurements }) => measurements.map((measurement) => ({ queue: queue.name, time: new Date(measurement.recorded_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }), people: measurement.person_count, wait: measurement.estimated_wait_time }))).sort((a, b) => a.time.localeCompare(b.time));
  const statusDistribution = Object.entries(data.reduce<Record<string, number>>((counts, { queue }) => ({ ...counts, [queue.status]: (counts[queue.status] ?? 0) + 1 }), {})).map(([name, value]) => ({ name, value }));
  const crowded = data.map(({ queue }) => ({ name: queue.name, density: Math.round(queue.density * 100) })).sort((a, b) => b.density - a.density);
  return <div className="space-y-6"><p className="text-sm text-slate-600">Analytics are assembled from the existing per-queue measurement API; a server-side aggregate endpoint can replace this client aggregation later.</p><section className="grid gap-6 xl:grid-cols-2"><ChartCard title="Queue population over time">{population.length ? <LineChart data={population}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line dataKey="people" name="People" stroke="#2563eb" /></LineChart> : <EmptyState label="No measurement history yet." />}</ChartCard><ChartCard title="Waiting time over time">{population.length ? <LineChart data={population}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line dataKey="wait" name="Minutes" stroke="#d97706" /></LineChart> : <EmptyState label="No measurement history yet." />}</ChartCard><ChartCard title="Queue status distribution"><PieChart><Pie data={statusDistribution} dataKey="value" nameKey="name" label>{statusDistribution.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}</Pie><Tooltip /></PieChart></ChartCard><ChartCard title="Most crowded queues"><BarChart data={crowded}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis unit="%" /><Tooltip /><Bar dataKey="density" name="Density" fill="#7c3aed" /></BarChart></ChartCard></section></div>;
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="mb-4 font-bold text-ink">{title}</h2><div className="h-72">{typeof children === "object" && children ? <ResponsiveContainer width="100%" height="100%">{children as React.ReactElement}</ResponsiveContainer> : children}</div></article>;
}
