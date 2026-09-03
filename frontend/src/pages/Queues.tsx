import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { ErrorState, LoadingState } from "../components/common/AsyncState";
import { QueueTable } from "../components/queues/QueueTable";
import { usePolling } from "../hooks/usePolling";
import { analyzeCameraFrame, createCamera, createQueue, deleteQueue, getLocations, getQueues, submitCameraObservation } from "../services/api";
import { useAuth } from "../hooks/useAuth";

function QueueAdminTools({ queues, locations, onCreated }: { queues: import("../types/api").Queue[]; locations: import("../types/api").Location[]; onCreated: () => void | Promise<void> }) {
  const { hasRole } = useAuth();
  const [message, setMessage] = useState<string | null>(null);
  const [cameraMessage, setCameraMessage] = useState<string | null>(null);
  const [cameras, setCameras] = useState<MediaDeviceInfo[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState("");
  const [selectedQueueId, setSelectedQueueId] = useState<number | "new">("new");
  const [cameraQueueName, setCameraQueueName] = useState("Camera Queue");
  const [cameraLocationId, setCameraLocationId] = useState("");
  const [cameraCapacity, setCameraCapacity] = useState("50");
  const [connectedCameraId, setConnectedCameraId] = useState<number | null>(null);
  const [automationEnabled, setAutomationEnabled] = useState(false);
  const video = useRef<HTMLVideoElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const stream = useRef<MediaStream | null>(null);

  useEffect(() => () => stream.current?.getTracks().forEach((track) => track.stop()), []);

  useEffect(() => {
    if (!connectedCameraId || !automationEnabled) return;
    let stopped = false;
    let inFlight = false;
    const captureAndAnalyze = async () => {
      const preview = video.current;
      const capture = canvas.current;
      if (stopped || inFlight || !preview || !capture || preview.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) return;
      inFlight = true;
      const width = Math.min(preview.videoWidth || 640, 640);
      const height = Math.max(1, Math.round((preview.videoHeight || 480) * (width / (preview.videoWidth || 640))));
      capture.width = width;
      capture.height = height;
      capture.getContext("2d")?.drawImage(preview, 0, 0, width, height);
      try {
        const observation = await analyzeCameraFrame(connectedCameraId, capture.toDataURL("image/jpeg", 0.7));
        if (!stopped) {
          setCameraMessage(`Live analysis: ${observation.person_count} people · ${(observation.density * 100).toFixed(0)}% density · ${observation.estimated_wait_time.toFixed(1)} min estimated wait.`);
          void onCreated();
        }
      } catch {
        if (!stopped) setCameraMessage("Live analysis could not process this frame. The preview remains connected; try again or check the backend camera-analysis service.");
      } finally { inFlight = false; }
    };
    void captureAndAnalyze();
    const timer = window.setInterval(() => void captureAndAnalyze(), 5_000);
    return () => { stopped = true; window.clearInterval(timer); };
  }, [automationEnabled, connectedCameraId, onCreated]);
  if (!hasRole("admin")) return null;
  async function addQueue(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); const form = new FormData(event.currentTarget);
    try { await createQueue({ name: String(form.get("name")), location_id: Number(form.get("location_id")), capacity: Number(form.get("capacity")), status: "NORMAL" }); event.currentTarget.reset(); setMessage("Queue created."); onCreated(); }
    catch { setMessage("Unable to create queue. Check the location ID and your administrator access."); }
  }
  async function connectCamera() {
    let queue = queues.find((item) => item.id === selectedQueueId);
    try {
      if (selectedQueueId === "new") {
        const locationId = Number(cameraLocationId);
        const capacity = Number(cameraCapacity);
        if (!cameraQueueName.trim() || !Number.isInteger(locationId) || locationId < 1 || !Number.isInteger(capacity) || capacity < 1) {
          setCameraMessage("Enter a queue name, valid location ID, and capacity to create a queue for this camera.");
          return;
        }
        queue = await createQueue({ name: cameraQueueName.trim(), location_id: locationId, capacity, status: "NORMAL" });
        setSelectedQueueId(queue.id);
        await onCreated();
      }
      if (!queue) { setCameraMessage("Select an existing queue or create one from this camera."); return; }
      stream.current?.getTracks().forEach((track) => track.stop());
      const cameraStream = await navigator.mediaDevices.getUserMedia({ video: selectedDeviceId ? { deviceId: { exact: selectedDeviceId } } : true, audio: false });
      stream.current = cameraStream;
      if (video.current) { video.current.srcObject = cameraStream; await video.current.play(); }
      const devices = (await navigator.mediaDevices.enumerateDevices()).filter((device) => device.kind === "videoinput");
      setCameras(devices);
      const selected = devices.find((device) => device.deviceId === (selectedDeviceId || cameraStream.getVideoTracks()[0]?.getSettings().deviceId));
      const camera = await createCamera({ name: selected?.label || "Browser camera", location_id: queue.location_id, queue_id: queue.id, source_type: "WEBCAM" });
      setConnectedCameraId(camera.id);
      setAutomationEnabled(true);
      setCameraMessage("Camera preview connected. Automatic analysis starts now; every reading is saved to this queue's historical analytics and published live.");
    } catch { setCameraMessage("Camera access was unavailable or denied. Allow browser camera permission and try again."); }
  }

  async function recordObservation(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!connectedCameraId) return;
    const form = new FormData(event.currentTarget);
    try {
      await submitCameraObservation(connectedCameraId, { person_count: Number(form.get("person_count")), density: Number(form.get("density")) });
      setCameraMessage("Observation saved. The queue status, analytics, forecast history, and live WebSocket update were refreshed.");
      void onCreated();
    } catch { setCameraMessage("Observation could not be submitted. Ensure the signed-in user can operate cameras."); }
  }
  return <section className="grid gap-5 rounded-xl border border-slate-200 bg-white p-5 shadow-sm lg:grid-cols-2"><form onSubmit={addQueue} className="space-y-3"><h2 className="font-bold text-ink">Add queue</h2><p className="text-sm text-slate-600">Queues are created as active (NORMAL).</p><input required name="name" defaultValue="General Enquiry" placeholder="Queue name" className="w-full rounded-md border border-slate-300 p-2" /><select required name="location_id" defaultValue="" className="w-full rounded-md border border-slate-300 p-2"><option value="" disabled>Select location</option>{locations.map((location) => <option key={location.id} value={location.id}>{location.name}</option>)}</select><input required name="capacity" type="number" min="1" defaultValue="50" placeholder="Capacity" className="w-full rounded-md border border-slate-300 p-2" /><button className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white">Create queue</button>{message && <p role="status" className="text-sm text-slate-600">{message}</p>}</form><div className="space-y-3"><h2 className="font-bold text-ink">Automatic camera monitoring</h2><p className="text-sm text-slate-600">Create a new queue directly from this camera or choose an existing one. Each five-second camera reading becomes historical analytics data and a live queue update.</p><select value={selectedQueueId} onChange={(event) => setSelectedQueueId(event.target.value === "new" ? "new" : Number(event.target.value))} className="w-full rounded-md border border-slate-300 p-2"><option value="new">Create a new queue from this camera</option>{queues.map((queue) => <option key={queue.id} value={queue.id}>{queue.name}</option>)}</select>{selectedQueueId === "new" && <div className="grid gap-2 rounded-md bg-slate-50 p-3"><input value={cameraQueueName} onChange={(event) => setCameraQueueName(event.target.value)} placeholder="New queue name" className="rounded-md border border-slate-300 p-2" /><select value={cameraLocationId} onChange={(event) => setCameraLocationId(event.target.value)} className="rounded-md border border-slate-300 p-2"><option value="">Select location</option>{locations.map((location) => <option key={location.id} value={location.id}>{location.name}</option>)}</select><input value={cameraCapacity} onChange={(event) => setCameraCapacity(event.target.value)} type="number" min="1" placeholder="Queue capacity" className="rounded-md border border-slate-300 p-2" /></div>}{cameras.length > 0 && <select value={selectedDeviceId} onChange={(event) => setSelectedDeviceId(event.target.value)} className="w-full rounded-md border border-slate-300 p-2"><option value="">Default camera</option>{cameras.map((camera, index) => <option key={camera.deviceId} value={camera.deviceId}>{camera.label || `Camera ${index + 1}`}</option>)}</select>}<button type="button" onClick={() => void connectCamera()} className="rounded-md bg-slate-800 px-4 py-2 text-sm font-semibold text-white">Create queue and connect camera</button><video ref={video} muted playsInline className="max-h-48 w-full rounded-md bg-slate-950 object-contain" /><canvas ref={canvas} className="hidden" />{connectedCameraId && <><button type="button" onClick={() => setAutomationEnabled((enabled) => !enabled)} className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700">{automationEnabled ? "Pause automatic analysis" : "Resume automatic analysis"}</button><form onSubmit={recordObservation} className="grid grid-cols-2 gap-2 rounded-md bg-slate-50 p-3"><input required name="person_count" min="0" type="number" placeholder="Manual people count" className="rounded-md border border-slate-300 p-2" /><input required name="density" min="0" max="1" step="0.01" type="number" placeholder="Manual density (0–1)" className="rounded-md border border-slate-300 p-2" /><button className="col-span-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white">Submit manual correction</button></form></>}{cameraMessage && <p role="status" className="text-sm text-slate-600">{cameraMessage}</p>}</div></section>;
}

export function Queues() {
  const { hasRole } = useAuth();
  const queueRequest = useCallback(() => getQueues(), []);
  const locationRequest = useCallback(() => getLocations(), []);
  const { data, error, loading, refresh } = usePolling(queueRequest);
  const { data: locations, error: locationError, loading: locationsLoading, refresh: refreshLocations } = usePolling(locationRequest);
  if (loading || locationsLoading) return <LoadingState label="Loading queues…" />;
  if (error || locationError || !data || !locations) return <ErrorState label={error ?? locationError ?? "Unable to load queues."} retry={async () => { await refresh(); await refreshLocations(); }} />;
  async function removeQueue(queue: import("../types/api").Queue) {
    try { await deleteQueue(queue.id); await refresh(); }
    catch { window.alert("Unable to delete this queue. Check that you are signed in as an administrator."); }
  }
  return <div className="space-y-5"><div><p className="text-sm text-slate-600">Search, filter, and open queues to inspect their measurement history.</p></div><QueueAdminTools queues={data} locations={locations} onCreated={refresh} /><QueueTable queues={data} onDelete={hasRole("admin") ? (queue) => void removeQueue(queue) : undefined} /></div>;
}
