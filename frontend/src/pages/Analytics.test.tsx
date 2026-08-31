import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { Analytics } from "./Analytics";

const { getQueueAnalytics } = vi.hoisted(() => ({ getQueueAnalytics: vi.fn() }));
vi.mock("../services/api", () => ({ getQueueAnalytics }));

describe("Analytics", () => {
  beforeEach(() => vi.clearAllMocks());

  it("uses the consolidated backend analytics response", async () => {
    getQueueAnalytics.mockResolvedValue([{ queue_id: 1, queue_name: "Security", measurement_count: 1, average_wait_time: 3, peak_person_count: 6, latest_measurement_at: "2026-09-01T10:00:00Z", measurements: [{ id: 1, queue_id: 1, person_count: 6, density: 0.3, estimated_wait_time: 3, status: "NORMAL", recorded_at: "2026-09-01T10:00:00Z" }] }]);
    render(<Analytics />);
    expect(await screen.findByText("Peak queue population")).toBeInTheDocument();
    expect(screen.getByText(/1 queue has recorded measurements/)).toBeInTheDocument();
  });
});
