import { afterEach, describe, expect, it, vi } from "vitest";
import { QueueWebSocket } from "./websocket";

vi.mock("./api", () => ({ getApiBaseUrl: () => "http://localhost:8000" }));

class MockWebSocket {
  static instances: MockWebSocket[] = [];
  onopen: (() => void) | null = null;
  onmessage: ((event: MessageEvent<string>) => void) | null = null;
  onclose: (() => void) | null = null;
  onerror: (() => void) | null = null;
  close = vi.fn(() => this.onclose?.());

  constructor(public readonly url: string, public readonly protocols?: string | string[]) {
    MockWebSocket.instances.push(this);
  }
}

describe("QueueWebSocket", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    MockWebSocket.instances = [];
  });

  it("reconnects with a bounded delay after an unexpected close", () => {
    vi.useFakeTimers();
    vi.stubGlobal("WebSocket", MockWebSocket);
    const statuses: string[] = [];
    const connection = new QueueWebSocket("test-token", (status) => statuses.push(status), vi.fn());

    connection.connect();
    expect(MockWebSocket.instances[0].protocols).toEqual("queueflow.jwt.test-token");
    MockWebSocket.instances[0].onopen?.();
    MockWebSocket.instances[0].onclose?.();
    expect(statuses).toEqual(["connecting", "live", "disconnected"]);

    vi.advanceTimersByTime(1_000);
    expect(MockWebSocket.instances).toHaveLength(2);
    expect(statuses.at(-1)).toBe("connecting");

    connection.close();
    vi.advanceTimersByTime(8_000);
    expect(MockWebSocket.instances).toHaveLength(2);
  });
});
