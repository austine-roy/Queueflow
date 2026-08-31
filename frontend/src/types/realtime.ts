import type { Alert, QueueStatus } from "./api";

export interface RealtimeQueue {
  id: number; name: string; current_count: number; density: number; estimated_wait_time: number; status: QueueStatus; timestamp: string;
}
export type RealtimeEvent = { type: "queue_update"; queue: RealtimeQueue } | { type: "alert"; alert: Alert };
export type ConnectionStatus = "connecting" | "live" | "disconnected";
