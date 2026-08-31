import { LogOut, RefreshCw, Radio, UserCircle, X } from "lucide-react";
import { Outlet, useLocation } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { useQueueWebSocket } from "../../hooks/useQueueWebSocket";
import { useAuth } from "../../hooks/useAuth";

const titles: Record<string, string> = { "/dashboard": "Overview", "/queues": "Queue monitoring", "/analytics": "Analytics", "/alerts": "Alerts", "/settings": "Settings" };

export function AppShell() {
  const location = useLocation();
  const { status, notifications, dismissAlert } = useQueueWebSocket();
  const { user, logout } = useAuth();
  const title = location.pathname.startsWith("/queues/") ? "Queue details" : titles[location.pathname] ?? "QueueFlow";
  return <div className="min-h-screen bg-cloud text-slate-900 md:flex"><Sidebar /><main className="min-w-0 flex-1"><header className="flex min-h-20 items-center justify-between border-b border-slate-200 bg-white px-5 pl-16 md:px-8"><div><h1 className="text-xl font-bold text-ink">{title}</h1><p className="text-xs text-slate-500">Queue monitoring workspace</p></div><div className="flex items-center gap-3"><span className={`hidden items-center gap-1.5 text-sm font-medium sm:flex ${status === "live" ? "text-emerald-700" : "text-slate-600"}`}><Radio size={17} aria-hidden="true" />{status === "live" ? "Live updates" : status === "connecting" ? "Connecting live updates" : "Live updates disconnected"}</span><button className="rounded-md border border-slate-200 p-2 text-slate-600" aria-label="Refresh current page" onClick={() => window.dispatchEvent(new Event("queueflow:refresh"))}><RefreshCw size={18} /></button><div className="hidden text-right text-xs text-slate-600 sm:block"><p className="font-semibold text-slate-800">{user?.email}</p><p className="capitalize">{user?.role}</p></div><UserCircle className="text-slate-500" aria-label="Current user" /><button className="rounded-md border border-slate-200 p-2 text-slate-600 hover:bg-slate-50" aria-label="Log out" onClick={() => void logout()}><LogOut size={18} /></button></div></header><div className="p-5 md:p-8"><Outlet /></div>{notifications.map((alert) => <div key={alert.id} role="alert" className="fixed bottom-4 right-4 flex max-w-sm items-start gap-3 rounded-lg bg-red-700 p-4 text-sm text-white shadow-lg"><span><b>{alert.severity}</b>: {alert.message}</span><button aria-label="Dismiss alert" onClick={() => dismissAlert(alert.id)}><X size={16} /></button></div>)}</main></div>;
}
