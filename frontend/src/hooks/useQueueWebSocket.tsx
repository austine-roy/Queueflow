/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { QueueWebSocket } from "../services/websocket";
import type { Alert, Queue } from "../types/api";
import type { ConnectionStatus, RealtimeQueue } from "../types/realtime";

interface RealtimeState { status: ConnectionStatus; latestQueue: RealtimeQueue | null; notifications: Alert[]; dismissAlert: (id: number) => void; }
const fallback: RealtimeState = { status: "disconnected", latestQueue: null, notifications: [], dismissAlert: () => undefined };
const Context = createContext<RealtimeState>(fallback);

export function QueueWebSocketProvider({ children }: { children: React.ReactNode }) {
  const [status, setStatus] = useState<ConnectionStatus>("connecting"); const [latestQueue, setLatestQueue] = useState<RealtimeQueue | null>(null); const [notifications, setNotifications] = useState<Alert[]>([]);
  useEffect(() => { const socket = new QueueWebSocket(setStatus, (event) => { if (event.type === "queue_update") setLatestQueue(event.queue); else setNotifications((items) => [event.alert, ...items.filter((item) => item.id !== event.alert.id)].slice(0, 3)); }); socket.connect(); return () => socket.close(); }, []);
  const value = useMemo(() => ({ status, latestQueue, notifications, dismissAlert: (id: number) => setNotifications((items) => items.filter((item) => item.id !== id)) }), [status, latestQueue, notifications]);
  return <Context.Provider value={value}>{children}</Context.Provider>;
}

export function useQueueWebSocket(): RealtimeState { return useContext(Context); }

export function mergeQueueUpdate(queues: Queue[], update: RealtimeQueue): Queue[] { return queues.map((queue) => queue.id === update.id ? { ...queue, ...update, updated_at: update.timestamp } : queue); }
