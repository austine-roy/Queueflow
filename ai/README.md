# AI Service

Milestone 5 provides a lightweight, independently testable video-file analysis baseline. It deliberately does not write to the database or broadcast events; Milestone 6 will connect its `QueueObservation` output to the established backend measurement publisher.

- `detection`: detector contracts and the optional OpenCV HOG baseline adapter
- `tracking`: deterministic centroid identity tracking
- `queue`: polygon queue regions, counting, and video orchestration
- `analytics`: bounded density and observation values
- `models`: local model metadata/adapters only; never commit weights
- `tests`: detector-independent unit and pipeline tests

## Run against a video file

Install the optional runtime dependency, then compose the detector, tracker, region, and analyzer in an application or script:

```bash
python -m pip install -r ai/requirements.txt
```

```python
from ai.detection import OpenCVHogPersonDetector
from ai.queue import QueueRegion
from ai.queue.video_pipeline import VideoQueueAnalyzer
from ai.tracking import CentroidTracker

analyzer = VideoQueueAnalyzer(
    OpenCVHogPersonDetector(),
    CentroidTracker(),
    QueueRegion("Security", ((0, 0), (1280, 0), (1280, 720), (0, 720))),
    capacity=30,
)
for observation in analyzer.analyze("sample.mp4"):
    print(observation)
```

The HOG detector is CPU-only and intended as a development baseline. Replace the `PersonDetector` implementation for production accuracy; keep model paths and video sources outside the repository configuration.
