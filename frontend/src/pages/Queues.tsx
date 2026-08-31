import { useCallback } from "react";
import { ErrorState, LoadingState } from "../components/common/AsyncState";
import { QueueTable } from "../components/queues/QueueTable";
import { usePolling } from "../hooks/usePolling";
import { getQueues } from "../services/api";

export function Queues() {
  const request = useCallback(() => getQueues(), []);
  const { data, error, loading, refresh } = usePolling(request);
  if (loading) return <LoadingState label="Loading queues…" />;
  if (error || !data) return <ErrorState label={error ?? "Unable to load queues."} retry={refresh} />;
  return <div className="space-y-5"><div><p className="text-sm text-slate-600">Search, filter, and open queues to inspect their measurement history.</p></div><QueueTable queues={data} /></div>;
}
