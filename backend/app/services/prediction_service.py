"""Small Random Forest queue-count forecast built from persisted measurements."""

from app.models.measurement import QueueMeasurement


def predict_next_count(measurements: list[QueueMeasurement], fallback: int) -> tuple[int, str]:
    """Forecast the next count; use a transparent fallback until enough history exists."""
    if len(measurements) < 5:
        return fallback, "insufficient_history"
    from sklearn.ensemble import RandomForestRegressor

    counts = [item.person_count for item in measurements]
    features = [[index, counts[index - 1]] for index in range(1, len(counts))]
    target = counts[1:]
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=1)
    model.fit(features, target)
    value = model.predict([[len(counts), counts[-1]]])[0]
    return max(0, round(float(value))), "random_forest"
