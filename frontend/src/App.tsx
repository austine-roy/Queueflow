import { Navigate, Route, Routes } from "react-router-dom";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { AppShell } from "./components/layout/AppShell";
import { Alerts } from "./pages/Alerts";
import { Analytics } from "./pages/Analytics";
import { Dashboard } from "./pages/Dashboard";
import { QueueDetails } from "./pages/QueueDetails";
import { Queues } from "./pages/Queues";
import { Settings } from "./pages/Settings";
import { QueueWebSocketProvider } from "./hooks/useQueueWebSocket";
import { AuthProvider } from "./hooks/useAuth";
import { Login, Unauthorized } from "./pages/Login";

export default function App() {
  return <AuthProvider><QueueWebSocketProvider><Routes><Route path="/login" element={<Login />} /><Route path="/unauthorized" element={<Unauthorized />} /><Route element={<ProtectedRoute><AppShell /></ProtectedRoute>}><Route index element={<Navigate to="/dashboard" replace />} /><Route path="dashboard" element={<Dashboard />} /><Route path="queues" element={<Queues />} /><Route path="queues/:id" element={<QueueDetails />} /><Route path="analytics" element={<Analytics />} /><Route path="alerts" element={<Alerts />} /><Route path="settings" element={<ProtectedRoute roles={["admin"]}><Settings /></ProtectedRoute>} /></Route><Route path="*" element={<Navigate to="/dashboard" replace />} /></Routes></QueueWebSocketProvider></AuthProvider>;
}
