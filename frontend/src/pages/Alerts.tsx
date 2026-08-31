import { useCallback, useState } from "react";
import { AlertCircle } from "lucide-react";
import { EmptyState, ErrorState, LoadingState } from "../components/common/AsyncState";
import { usePolling } from "../hooks/usePolling";
import { getAlerts } from "../services/api";
import { formatDate } from "../utils/format";

export function Alerts() {
  const [filter, setFilter] = useState<"ALL" | "ACTIVE" | "RESOLVED">("ALL");
  const request = useCallback(() => getAlerts(), []);
  const { data, error, loading, refresh } = usePolling(request);
  if (loading) return <LoadingState label="Loading alerts…" />;
  if (error || !data) return <ErrorState label="Alerts are unavailable because the current backend does not expose an alert-list API yet." retry={refresh} />;
  const shown = data.filter((alert) => filter === "ALL" || (filter === "ACTIVE" ? alert.is_active : !alert.is_active));
  if (!data.length) return <EmptyState label="No alerts found." />;
  return <div className="space-y-5"><div className="flex flex-wrap gap-2" aria-label="Alert filters">{(["ALL", "ACTIVE", "RESOLVED"] as const).map((option) => <button key={option} onClick={() => setFilter(option)} className={`rounded-full px-3 py-1.5 text-sm font-semibold ${filter === option ? "bg-blue-600 text-white" : "bg-white text-slate-600 ring-1 ring-slate-200"}`}>{option[0] + option.slice(1).toLowerCase()}</button>)}</div>{shown.length ? <div className="space-y-3">{shown.map((alert) => <article key={alert.id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"><div className="flex gap-3"><AlertCircle className="mt-0.5 text-amber-600" aria-hidden="true" /><div className="min-w-0 flex-1"><div className="flex flex-wrap items-center justify-between gap-2"><h2 className="font-bold">{alert.type}</h2><span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-bold">{alert.severity}</span></div><p className="mt-1 text-slate-700">{alert.message}</p><p className="mt-2 text-xs text-slate-500">Queue #{alert.queue_id} · {formatDate(alert.created_at)} · {alert.is_active ? "Active" : "Resolved"}</p></div></div></article>)}</div> : <EmptyState label="No alerts match this filter." />}</div>;
}
