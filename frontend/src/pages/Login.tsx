import { FormEvent, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState(""); const [password, setPassword] = useState(""); const [error, setError] = useState<string | null>(null); const [loading, setLoading] = useState(false);
  if (user) return <Navigate to="/dashboard" replace />;
  async function submit(event: FormEvent) {
    event.preventDefault(); setError(null); setLoading(true);
    try { await login(email, password); navigate((location.state as { from?: string } | null)?.from ?? "/dashboard", { replace: true }); }
    catch { setError("Invalid email or password."); }
    finally { setLoading(false); }
  }
  return <main className="flex min-h-screen items-center justify-center bg-cloud p-5"><form onSubmit={submit} className="w-full max-w-md space-y-5 rounded-xl border border-slate-200 bg-white p-7 shadow-sm"><div><h1 className="text-2xl font-bold text-ink">Queue<span className="text-blue-600">Flow</span></h1><p className="mt-1 text-sm text-slate-600">Sign in to access queue operations.</p></div>{error && <p role="alert" className="rounded-md bg-red-50 p-3 text-sm text-red-800">{error}</p>}<label className="block text-sm font-semibold text-slate-700">Email<input required type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-1 block w-full rounded-md border border-slate-300 p-2 font-normal" /></label><label className="block text-sm font-semibold text-slate-700">Password<input required type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-1 block w-full rounded-md border border-slate-300 p-2 font-normal" /></label><button disabled={loading} className="w-full rounded-md bg-blue-600 px-4 py-2 font-semibold text-white disabled:opacity-60">{loading ? "Signing in…" : "Sign in"}</button></form></main>;
}

export function Unauthorized() { return <main className="flex min-h-screen items-center justify-center bg-cloud p-5"><section className="max-w-md rounded-xl border border-amber-200 bg-white p-7 text-center shadow-sm"><h1 className="text-2xl font-bold text-ink">Access denied</h1><p className="mt-2 text-slate-600">Your role does not have permission to open this page.</p></section></main>; }
