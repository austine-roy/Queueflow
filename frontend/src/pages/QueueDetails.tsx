import { ArrowLeft, History, Users } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { EmptyState, ErrorState, LoadingState } from "../components/common/AsyncState";
import { StatusBadge } from "../components/common/StatusBadge";
import { usePolling } from "../hooks/usePolling";
import { getAlerts, getMeasurements, getQueue } from "../services/api";
import { formatDate, formatPercentage, formatWait, locationLabel } from "../utils/format";
import { useQueueWebSocket } from "../hooks/useQueueWebSocket";
import type { Queue } from "../types/api";

export function QueueDetails() {
  const id = Number(useParams().id);
  const request = useCallback(async () => {
    const [queue, measurements, alerts] = await Promise.all([getQueue(id), getMeasurements(id), getAlerts().catch(() => null)]);
    return { queue, measurements: [...measurements].reverse(), alerts: alerts?.filter((alert) => alert.queue_id === id) ?? null };
  }, [id]);
  const { data, error, loading, refresh } = usePolling(request);
  const [liveQueue, setLiveQueue] = useState<Queue | null>(null);
  const { latestQueue } = useQueueWebSocket();
  useEffect(() => { if (data) setLiveQueue(data.queue); }, [data]);
  useEffect(() => { if (latestQueue?.id === id) setLiveQueue((queue) => queue ? { ...queue, ...latestQueue, updated_at: latestQueue.timestamp } : queue); }, [latestQueue, id]);
  const chartData = useMemo(() => data?.measurements.map((measurement) => ({ ...measurement, time: new Date(measurement.recorded_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) })) ?? [], [data]);
  if (!Number.isInteger(id) || id <= 0) return <ErrorState label="This queue identifier is invalid." />;
  if (loading) return <LoadingState label="Loading queue details…" />;
  if (error || !data) return <ErrorState label={error ?? "Unable to load queue details."} retry={refresh} />;
  const queue = liveQueue ?? data.queue;
  return <div className="space-y-6"><Link to="/queues" className="inline-flex items-center gap-1 text-sm font-semibold text-blue-700"><ArrowLeft size={16} />Back to queues</Link><section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex flex-col justify-between gap-4 sm:flex-row"><div><h2 className="text-2xl font-bold text-ink">{queue.name}</h2><p className="mt-1 text-sm text-slate-500">{locationLabel(queue.location_id)}</p></div><StatusBadge status={queue.status} /></div><dl className="mt-6 grid grid-cols-2 gap-4 text-sm md:grid-cols-4"><div><dt className="text-slate-500">Current people</dt><dd className="mt-1 text-xl font-bold">{queue.current_count}</dd></div><div><dt className="text-slate-500">Capacity</dt><dd className="mt-1 text-xl font-bold">{queue.capacity}</dd></div><div><dt className="text-slate-500">Density</dt><dd className="mt-1 text-xl font-bold">{formatPercentage(queue.density)}</dd></div><div><dt className="text-slate-500">Estimated wait</dt><dd className="mt-1 text-xl font-bold">{formatWait(queue.estimated_wait_time)}</dd></div></dl></section><section className="grid gap-6 xl:grid-cols-2">{["person_count", "estimated_wait_time"].map((field) => <article key={field} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="font-bold text-ink">{field === "person_count" ? "People count" : "Estimated waiting time"}</h2><p className="mb-4 text-sm text-slate-500">Historical measurements from the QueueFlow API</p>{chartData.length ? <div className="h-64"><ResponsiveContainer width="100%" height="100%"><LineChart data={chartData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line type="monotone" dataKey={field} name={field === "person_count" ? "People" : "Minutes"} stroke={field === "person_count" ? "#2563eb" : "#d97706"} strokeWidth={2} /></LineChart></ResponsiveContainer></div> : <EmptyState label="No historical measurements are available yet." />}</article>)}</section><section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-center gap-2"><History size={19} /><h2 className="font-bold text-ink">Measurement history</h2></div>{data.measurements.length ? <ol className="mt-4 divide-y divide-slate-100">{data.measurements.slice().reverse().map((measurement) => <li key={measurement.id} className="flex justify-between gap-4 py-3 text-sm"><span><Users className="mr-1 inline" size={15} />{measurement.person_count} people · {formatWait(measurement.estimated_wait_time)}</span><time className="text-slate-500">{formatDate(measurement.recorded_at)}</time></li>)}</ol> : <p className="mt-3 text-sm text-slate-500">No measurements have been recorded.</p>}</section><section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="font-bold text-ink">Associated alerts</h2>{data.alerts === null ? <p className="mt-2 text-sm text-slate-600">Alerts cannot be shown yet because the current backend has no alert-list endpoint.</p> : data.alerts.length ? <ul className="mt-3 space-y-2">{data.alerts.map((alert) => <li key={alert.id}>{alert.message}</li>)}</ul> : <p className="mt-2 text-sm text-slate-500">No alerts for this queue.</p>}</section></div>;
}
