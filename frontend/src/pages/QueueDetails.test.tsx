import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { QueueDetails } from "./QueueDetails";

vi.mock("../services/api", () => ({
  getQueue: vi.fn().mockResolvedValue({ id: 1, name: "Security", location_id: 1, capacity: 20, status: "NORMAL", current_count: 5, density: 0.25, estimated_wait_time: 2.5, created_at: "2026-08-24T10:00:00Z", updated_at: "2026-08-24T10:00:00Z" }),
  getMeasurements: vi.fn().mockResolvedValue([{ id: 1, queue_id: 1, person_count: 5, density: 0.25, estimated_wait_time: 2.5, status: "NORMAL", recorded_at: "2026-08-24T10:00:00Z" }]),
  getAlerts: vi.fn().mockRejectedValue(new Error("not implemented"))
}));

describe("QueueDetails", () => {
  it("loads the queue and its historical measurements", async () => {
    render(<MemoryRouter initialEntries={["/queues/1"]}><Routes><Route path="/queues/:id" element={<QueueDetails />} /></Routes></MemoryRouter>);
    expect(await screen.findByText("Security")).toBeInTheDocument();
    expect(screen.getByText("People count")).toBeInTheDocument();
    expect(screen.getByText(/Alerts cannot be shown yet/)).toBeInTheDocument();
  });
});
