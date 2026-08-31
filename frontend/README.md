# QueueFlow frontend

The QueueFlow dashboard is a React + TypeScript + Vite application styled with Tailwind CSS. It uses Axios to query the backend, Recharts for measurement visualizations, Lucide icons, and browser polling (10 seconds by default).

## Requirements

- Node.js 20+
- QueueFlow backend running at the configured API URL

## Setup

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The development dashboard is available at `http://localhost:5173`.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `VITE_API_BASE_URL` | Backend origin, e.g. `http://localhost:8000` |
| `VITE_REFRESH_INTERVAL_SECONDS` | Polling interval; defaults to `10` |

The backend's `FRONTEND_ORIGIN` must allow the dashboard origin for browser requests.

The dashboard connects to the backend at `/ws/queues` and displays its live-connection state. On an unavailable or dropped connection, it uses exponential reconnection delays capped at eight seconds while ordinary REST polling continues to refresh queue data.

## Commands

```bash
npm run dev      # development server
npm run lint     # ESLint
npm test         # Vitest component/page tests
npm run build    # production build
```

## API limitations

The current backend exposes queues, per-queue measurements, alerts, and real-time queue events. Location names are not yet included in queue API responses, so the dashboard renders `Location #<id>`.
