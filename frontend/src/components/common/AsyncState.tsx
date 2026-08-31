import { AlertCircle, Inbox, LoaderCircle } from "lucide-react";

export function LoadingState({ label = "Loading queue data…" }: { label?: string }) {
  return <div className="flex min-h-40 items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white p-8 text-slate-600"><LoaderCircle className="animate-spin" aria-hidden="true" />{label}</div>;
}

export function EmptyState({ label }: { label: string }) {
  return <div className="flex min-h-40 flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-slate-300 bg-white p-8 text-slate-600"><Inbox aria-hidden="true" />{label}</div>;
}

export function ErrorState({ label, retry }: { label: string; retry?: () => void }) {
  return <div role="alert" className="flex min-h-40 flex-col items-center justify-center gap-3 rounded-xl border border-red-200 bg-red-50 p-8 text-center text-red-800"><AlertCircle aria-hidden="true" />{label}{retry && <button className="rounded-md bg-red-700 px-3 py-1.5 text-sm font-semibold text-white" onClick={retry}>Retry</button>}</div>;
}
