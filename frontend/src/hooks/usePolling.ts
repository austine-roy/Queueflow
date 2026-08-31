import { useCallback, useEffect, useState } from "react";

export interface QueryState<T> {
  data: T | null;
  error: string | null;
  loading: boolean;
  refresh: () => Promise<void>;
}

const defaultInterval = Number(globalThis.localStorage?.getItem("queueflow.refreshInterval") ?? import.meta.env.VITE_REFRESH_INTERVAL_SECONDS ?? 10) * 1_000;

export function usePolling<T>(request: () => Promise<T>, interval = defaultInterval): QueryState<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setError(null);
    try {
      setData(await request());
    } catch {
      setError("Unable to load queue data. Check the API server and try again.");
    } finally {
      setLoading(false);
    }
  }, [request]);

  useEffect(() => {
    void refresh();
    const timer = window.setInterval(() => void refresh(), interval);
    return () => window.clearInterval(timer);
  }, [interval, refresh]);

  useEffect(() => {
    const onRefresh = () => void refresh();
    window.addEventListener("queueflow:refresh", onRefresh);
    return () => window.removeEventListener("queueflow:refresh", onRefresh);
  }, [refresh]);

  return { data, error, loading, refresh };
}
