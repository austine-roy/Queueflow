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

## Commands

```bash
npm run dev      # development server
npm run lint     # ESLint
npm test         # Vitest component/page tests
npm run build    # production build
```

## API limitations in Milestone 3

The current backend exposes queues and per-queue measurements. It does not yet expose location names or an alert-list API. The dashboard accurately renders `Location #<id>`, aggregates measurements client-side for analytics, and explains when alerts are unavailable instead of showing fabricated data.
