import { BarChart3, Bell, LayoutDashboard, Menu, Settings, X } from "lucide-react";
import { NavLink } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import type { UserRole } from "../../types/api";

const links: Array<{ to: string; label: string; icon: typeof LayoutDashboard; roles?: UserRole[] }> = [{ to: "/dashboard", label: "Dashboard", icon: LayoutDashboard }, { to: "/queues", label: "Queues", icon: Menu }, { to: "/analytics", label: "Analytics", icon: BarChart3 }, { to: "/alerts", label: "Alerts", icon: Bell }, { to: "/settings", label: "Settings", icon: Settings, roles: ["admin"] }];

function NavItems({ onNavigate }: { onNavigate?: () => void }) {
  const { hasRole } = useAuth();
  return <nav aria-label="Main navigation" className="space-y-1">{links.filter((link) => !link.roles || hasRole(...link.roles)).map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} onClick={onNavigate} className={({ isActive }) => `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-semibold ${isActive ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-white/10 hover:text-white"}`}><Icon size={18} aria-hidden="true" />{label}</NavLink>)}</nav>;
}

export function Sidebar() {
  const [open, setOpen] = useState(false);
  return <><button className="fixed left-4 top-4 z-30 rounded-md bg-ink p-2 text-white md:hidden" aria-label="Open navigation" onClick={() => setOpen(true)}><Menu /></button><aside className="hidden min-h-screen w-60 shrink-0 bg-ink p-5 md:block"><p className="mb-10 text-xl font-bold text-white">Queue<span className="text-blue-400">Flow</span></p><NavItems /></aside>{open && <div className="fixed inset-0 z-40 bg-slate-950/40 md:hidden" onClick={() => setOpen(false)}><aside className="h-full w-64 bg-ink p-5" onClick={(event) => event.stopPropagation()}><button className="mb-8 ml-auto block text-white" aria-label="Close navigation" onClick={() => setOpen(false)}><X /></button><p className="mb-10 text-xl font-bold text-white">Queue<span className="text-blue-400">Flow</span></p><NavItems onNavigate={() => setOpen(false)} /></aside></div>}</>;
}
