import { AlertTriangle, CheckCircle2, CircleOff, Flame, Users } from "lucide-react";
import type { QueueStatus } from "../../types/api";

const styles: Record<QueueStatus, string> = {
  NORMAL: "bg-emerald-50 text-emerald-800 ring-emerald-200",
  BUSY: "bg-amber-50 text-amber-800 ring-amber-200",
  CROWDED: "bg-orange-50 text-orange-800 ring-orange-200",
  CRITICAL: "bg-red-50 text-red-800 ring-red-200",
  CLOSED: "bg-slate-100 text-slate-700 ring-slate-200"
};
const icons: Record<QueueStatus, typeof CheckCircle2> = { NORMAL: CheckCircle2, BUSY: Users, CROWDED: AlertTriangle, CRITICAL: Flame, CLOSED: CircleOff };

export function StatusBadge({ status }: { status: QueueStatus }) {
  const Icon = icons[status];
  return <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold ring-1 ${styles[status]}`}><Icon size={14} aria-hidden="true" />{status}</span>;
}
