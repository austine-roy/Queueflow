import { getApiBaseUrl } from "./api";
import type { RealtimeEvent } from "../types/realtime";

export function getQueueWebSocketUrl(): string {
  const url = new URL(getApiBaseUrl(), window.location.origin);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  url.pathname = "/ws/queues";
  return url.toString();
}

export class QueueWebSocket {
  private socket: WebSocket | null = null; private retry = 0; private timer: number | null = null; private closed = false;
  constructor(private readonly onStatus: (status: "connecting" | "live" | "disconnected") => void, private readonly onEvent: (event: RealtimeEvent) => void) {}
  connect(): void {
    this.closed = false; this.onStatus("connecting");
    this.socket = new WebSocket(getQueueWebSocketUrl());
    this.socket.onopen = () => { this.retry = 0; this.onStatus("live"); };
    this.socket.onmessage = (message) => { try { this.onEvent(JSON.parse(message.data) as RealtimeEvent); } catch { /* ignore malformed events */ } };
    this.socket.onclose = () => { if (!this.closed) this.scheduleReconnect(); else this.onStatus("disconnected"); };
    this.socket.onerror = () => this.socket?.close();
  }
  private scheduleReconnect(): void { this.onStatus("disconnected"); const delay = Math.min(1_000 * 2 ** this.retry++, 8_000); this.timer = window.setTimeout(() => this.connect(), delay); }
  close(): void { this.closed = true; if (this.timer !== null) window.clearTimeout(this.timer); this.socket?.close(); }
}
