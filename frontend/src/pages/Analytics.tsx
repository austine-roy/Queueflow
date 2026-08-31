import { useCallback } from "react";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { EmptyState, ErrorState, LoadingState } from "../components/common/AsyncState";
import { usePolling } from "../hooks/usePolling";
import { getQueueAnalytics } from "../services/api";

export function Analytics() {
  const request = useCallback(() => getQueueAnalytics(), []);
  const { data, error, loading, refresh } = usePolling(request);
  if (loading) return <LoadingState label="Loading analytics…" />;
  if (error || !data) return <ErrorState label={error ?? "Unable to load analytics."} retry={refresh} />;
  if (!data.length) return <EmptyState label="No queues found. Analytics will appear when queues are registered." />;
  const population = data.flatMap(({ queue_name, measurements }) => measurements.map((measurement) => ({ queue: queue_name, time: new Date(measurement.recorded_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }), people: measurement.person_count, wait: measurement.estimated_wait_time }))).sort((a, b) => a.time.localeCompare(b.time));
  const historyAvailability = data.filter((item) => item.measurement_count > 0).length;
  return <div className="space-y-6"><p className="text-sm text-slate-600">Analytics are aggregated by the backend from persisted queue history. {historyAvailability} queue{historyAvailability === 1 ? " has" : "s have"} recorded measurements.</p><section className="grid gap-6 xl:grid-cols-2"><ChartCard title="Queue population over time">{population.length ? <LineChart data={population}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line dataKey="people" name="People" stroke="#2563eb" /></LineChart> : <EmptyState label="No measurement history yet." />}</ChartCard><ChartCard title="Waiting time over time">{population.length ? <LineChart data={population}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line dataKey="wait" name="Minutes" stroke="#d97706" /></LineChart> : <EmptyState label="No measurement history yet." />}</ChartCard><ChartCard title="Peak queue population"><BarChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="queue_name" /><YAxis /><Tooltip /><Bar dataKey="peak_person_count" name="Peak people" fill="#7c3aed" /></BarChart></ChartCard><ChartCard title="Average waiting time"><BarChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="queue_name" /><YAxis /><Tooltip /><Bar dataKey="average_wait_time" name="Minutes" fill="#10b981" /></BarChart></ChartCard></section></div>;
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="mb-4 font-bold text-ink">{title}</h2><div className="h-72">{typeof children === "object" && children ? <ResponsiveContainer width="100%" height="100%">{children as React.ReactElement}</ResponsiveContainer> : children}</div></article>;
}
