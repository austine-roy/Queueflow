import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { QueueTable } from "./QueueTable";

const queue = { id: 1, name: "Security", location_id: 2, capacity: 20, status: "BUSY" as const, current_count: 12, density: 0.6, estimated_wait_time: 6, created_at: "2026-08-24T10:00:00Z", updated_at: "2026-08-24T10:00:00Z" };

describe("QueueTable", () => {
  it("shows API queue data and links to its detail page", () => {
    render(<MemoryRouter><QueueTable queues={[queue]} /></MemoryRouter>);
    expect(screen.getByRole("link", { name: "Security" })).toHaveAttribute("href", "/queues/1");
    expect(screen.getByText("Location #2")).toBeInTheDocument();
    expect(screen.getByText("BUSY", { selector: "span" })).toBeInTheDocument();
  });

  it("offers a confirmed delete action when the caller authorizes it", () => {
    const onDelete = vi.fn();
    vi.spyOn(window, "confirm").mockReturnValue(true);
    render(<MemoryRouter><QueueTable queues={[queue]} onDelete={onDelete} /></MemoryRouter>);
    fireEvent.click(screen.getByRole("button", { name: "Delete Security" }));
    expect(onDelete).toHaveBeenCalledWith(queue);
  });
});
