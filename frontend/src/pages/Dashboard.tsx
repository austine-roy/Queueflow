import { AlertTriangle, Clock3, ListChecks, Users } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { MetricCard } from "../components/dashboard/MetricCard";
import { EmptyState, ErrorState, LoadingState } from "../components/common/AsyncState";
import { StatusBadge } from "../components/common/StatusBadge";
import { usePolling } from "../hooks/usePolling";
import { getQueues } from "../services/api";
import { formatWait } from "../utils/format";
import { mergeQueueUpdate, useQueueWebSocket } from "../hooks/useQueueWebSocket";

export function Dashboard() {
  const loadQueues = useCallback(() => getQueues(), []);
  const { data: queues, error, loading, refresh } = usePolling(loadQueues);
  const [liveQueues, setLiveQueues] = useState(queues ?? []);
  const { latestQueue, status } = useQueueWebSocket();
  useEffect(() => { if (queues) setLiveQueues(queues); }, [queues]);
  useEffect(() => { if (latestQueue) setLiveQueues((items) => mergeQueueUpdate(items, latestQueue)); }, [latestQueue]);
  if (loading) return <LoadingState label="Loading dashboard…" />;
  if (error || !queues) return <ErrorState label={error ?? "Unable to load dashboard."} retry={refresh} />;
  if (!liveQueues.length) return <EmptyState label="No queues found. Add queue data through the backend API to begin monitoring." />;
  const active = liveQueues.filter((queue) => queue.status !== "CLOSED");
  const people = active.reduce((sum, queue) => sum + queue.current_count, 0);
  const averageWait = active.length ? active.reduce((sum, queue) => sum + queue.estimated_wait_time, 0) / active.length : 0;
  const critical = liveQueues.filter((queue) => queue.status === "CRITICAL").length;
  return <div className="space-y-6"><section><p className="text-sm text-slate-600">{status === "live" ? "Live queue updates connected." : "Live updates unavailable; REST polling remains active."}</p><div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-4"><MetricCard label="Total queues" value={liveQueues.length} detail={`${active.length} active`} icon={ListChecks} /><MetricCard label="People waiting" value={people} detail="Across active queues" icon={Users} /><MetricCard label="Average wait" value={formatWait(averageWait)} detail="Service-rate estimate" icon={Clock3} /><MetricCard label="Critical queues" value={critical} detail={critical ? "Needs immediate attention" : "No critical queues"} icon={AlertTriangle} /></div></section><section className="grid gap-6 xl:grid-cols-[1.15fr_.85fr]"><div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><div className="mb-5"><h2 className="font-bold text-ink">Queue status</h2><p className="text-sm text-slate-500">Current API measurements</p></div><div className="space-y-3">{liveQueues.slice(0, 6).map((queue) => <div className="flex items-center justify-between gap-3 rounded-lg bg-slate-50 p-3" key={queue.id}><div><p className="font-semibold">{queue.name}</p><p className="text-sm text-slate-500">{queue.current_count} people · {formatWait(queue.estimated_wait_time)}</p></div><StatusBadge status={queue.status} /></div>)}</div></div><div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"><h2 className="font-bold text-ink">Current queue analytics</h2><p className="mb-4 text-sm text-slate-500">People currently recorded per queue</p><div className="h-72"><ResponsiveContainer width="100%" height="100%"><BarChart data={liveQueues}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} angle={-20} textAnchor="end" height={65} /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="current_count" name="People" fill="#2563eb" radius={[4, 4, 0, 0]} /></BarChart></ResponsiveContainer></div></div></section></div>;
}
