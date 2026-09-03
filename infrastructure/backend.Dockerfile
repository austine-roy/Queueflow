FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=120

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
# Ultralytics declares the desktop OpenCV package. Replace it with the headless
# build already pinned by QueueFlow so slim containers do not require GUI/X11
# libraries.
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall --yes opencv-python \
    && pip install --no-cache-dir --force-reinstall opencv-python-headless==4.10.0.84 \
    && python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')" \
    && useradd --create-home --uid 10001 queueflow

COPY backend/ ./
RUN chown -R queueflow:queueflow /app

USER queueflow
EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
