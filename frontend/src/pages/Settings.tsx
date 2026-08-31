import { FormEvent, useState } from "react";
import { getApiBaseUrl, saveApiBaseUrl } from "../services/api";

export function Settings() {
  const [apiUrl, setApiUrl] = useState(getApiBaseUrl());
  const [interval, setIntervalValue] = useState(localStorage.getItem("queueflow.refreshInterval") ?? import.meta.env.VITE_REFRESH_INTERVAL_SECONDS ?? "10");
  const [saved, setSaved] = useState(false);
  function submit(event: FormEvent) { event.preventDefault(); saveApiBaseUrl(apiUrl); localStorage.setItem("queueflow.refreshInterval", interval); setSaved(true); }
  return <form onSubmit={submit} className="max-w-2xl space-y-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm"><div><h2 className="text-lg font-bold text-ink">Application settings</h2><p className="mt-1 text-sm text-slate-600">Settings are saved only in this browser. Access to this page is restricted to administrators.</p></div><label className="block text-sm font-semibold text-slate-700">API server URL<input type="url" value={apiUrl} onChange={(event) => { setApiUrl(event.target.value); setSaved(false); }} placeholder="http://localhost:8000" className="mt-2 block w-full rounded-md border border-slate-300 p-2 font-normal" /></label><label className="block text-sm font-semibold text-slate-700">Refresh interval (seconds)<input type="number" min="5" value={interval} onChange={(event) => { setIntervalValue(event.target.value); setSaved(false); }} className="mt-2 block w-32 rounded-md border border-slate-300 p-2 font-normal" /></label><button className="rounded-md bg-blue-600 px-4 py-2 font-semibold text-white">Save preferences</button>{saved && <p role="status" className="text-sm text-emerald-700">Preferences saved. Refresh the page to apply a changed polling interval.</p>}</form>;
}
