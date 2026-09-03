import { useCallback } from "react";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { EmptyState, ErrorState, LoadingState } from "../components/common/AsyncState";
import { usePolling } from "../hooks/usePolling";
import { getQueueAnalytics, getQueuePrediction } from "../services/api";

type AnalyticsData = { analytics: Awaited<ReturnType<typeof getQueueAnalytics>>; predictions: Awaited<ReturnType<typeof getQueuePrediction>>[] };

export function Analytics() {
  const request = useCallback(async (): Promise<AnalyticsData> => {
    const analytics = await getQueueAnalytics();
    const predictions = await Promise.all(analytics.map((queue) => getQueuePrediction(queue.queue_id)));
    return { analytics, predictions };
  }, []);
  const { data, error, loading, refresh } = usePolling(request);
  if (loading) return <LoadingState label="Loading analytics…" />;
  if (error || !data) return <ErrorState label={error ?? "Unable to load analytics."} retry={refresh} />;
  if (!data.analytics.length) return <EmptyState label="No queues found. Analytics will appear when queues are registered." />;
  const { analytics, predictions } = data;
  const population = analytics.flatMap(({ queue_name, measurements }) => measurements.map((measurement) => ({ queue: queue_name, time: new Date(measurement.recorded_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }), people: measurement.person_count, wait: measurement.estimated_wait_time }))).sort((a, b) => a.time.localeCompare(b.time));
  const historyAvailability = analytics.filter((item) => item.measurement_count > 0).length;
  const totalMeasurements = analytics.reduce((total, item) => total + item.measurement_count, 0);
  const peakPopulation = Math.max(...analytics.map((item) => item.peak_person_count));
  const averageWait = analytics.reduce((total, item) => total + item.average_wait_time, 0) / analytics.length;
  return <div className="space-y-6"><p className="text-sm text-slate-600">Analytics are aggregated by the backend from persisted queue history. {historyAvailability} queue{historyAvailability === 1 ? " has" : "s have"} recorded measurements.</p><section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4"><Statistic label="Queues" value={analytics.length} /><Statistic label="Measurements" value={totalMeasurements} /><Statistic label="Peak population" value={peakPopulation} /><Statistic label="Average wait" value={`${averageWait.toFixed(1)} min`} /></section><section className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">{predictions.map((prediction) => <article key={prediction.queue_id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"><p className="text-sm text-slate-500">Next count forecast · {analytics.find((queue) => queue.queue_id === prediction.queue_id)?.queue_name}</p><p className="mt-1 text-2xl font-bold text-ink">{prediction.predicted_count} people</p><p className="text-sm text-slate-600">{prediction.model === "random_forest" ? `Random Forest regression · ${prediction.measurement_count} observations` : `Needs 5 observations · ${prediction.measurement_count} recorded`}</p></article>)}</section><section className="grid gap-6 xl:grid-cols-2"><ChartCard title="Queue population over time">{population.length ? <LineChart data={population}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line dataKey="people" name="People" stroke="#2563eb" /></LineChart> : <EmptyState label="No measurement history yet." />}</ChartCard><ChartCard title="Waiting time over time">{population.length ? <LineChart data={population}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line dataKey="wait" name="Minutes" stroke="#d97706" /></LineChart> : <EmptyState label="No measurement history yet." />}</ChartCard><ChartCard title="Peak queue population"><BarChart data={analytics}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="queue_name" /><YAxis /><Tooltip /><Bar dataKey="peak_person_count" name="Peak people" fill="#7c3aed" /></BarChart></ChartCard><ChartCard title="Average waiting time"><BarChart data={analytics}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="queue_name" /><YAxis /><Tooltip /><Bar dataKey="average_wait_time" name="Minutes" fill="#10b981" /></BarChart></ChartCard></section></div>;
}

function Statistic({ label, value }: { label: string; value: string | number }) {
  return <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"><p className="text-sm text-slate-500">{label}</p><p className="mt-1 text-2xl font-bold text-ink">{value}</p></article>;
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="mb-4 font-bold text-ink">{title}</h2><div className="h-72">{typeof children === "object" && children ? <ResponsiveContainer width="100%" height="100%">{children as React.ReactElement}</ResponsiveContainer> : children}</div></article>;
}
