import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { Dashboard } from "./Dashboard";

const { getQueues } = vi.hoisted(() => ({ getQueues: vi.fn() }));
vi.mock("../services/api", () => ({ getQueues }));

describe("Dashboard", () => {
  beforeEach(() => vi.clearAllMocks());

  it("renders calculated metric cards from queue data", async () => {
    getQueues.mockResolvedValue([{ id: 1, name: "Security", location_id: 1, capacity: 20, status: "CRITICAL", current_count: 18, density: 0.9, estimated_wait_time: 9, created_at: "2026-08-24T10:00:00Z", updated_at: "2026-08-24T10:00:00Z" }]);
    render(<Dashboard />);
    expect(await screen.findByText("People waiting")).toBeInTheDocument();
    expect(screen.getByText("Critical queues")).toBeInTheDocument();
    expect(screen.getByText("Security")).toBeInTheDocument();
  });

  it("shows an error state when the API fails", async () => {
    getQueues.mockRejectedValue(new Error("offline"));
    render(<Dashboard />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Unable to load queue data");
  });
});
