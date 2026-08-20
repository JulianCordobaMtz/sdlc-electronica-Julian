from collections import defaultdict
from threading import Lock


class MetricsRegistry:
    """Registro mínimo de métricas HTTP en formato Prometheus."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._request_count: dict[tuple[str, str, int], int] = defaultdict(int)
        self._request_duration: dict[tuple[str, str], tuple[int, float]] = defaultdict(
            lambda: (0, 0.0)
        )

    def observe(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_seconds: float,
    ) -> None:
        with self._lock:
            self._request_count[(method, path, status_code)] += 1
            count, total = self._request_duration[(method, path)]
            self._request_duration[(method, path)] = (
                count + 1,
                total + duration_seconds,
            )

    def render(self) -> str:
        lines = [
            "# HELP sensorhub_http_requests_total Total de solicitudes HTTP.",
            "# TYPE sensorhub_http_requests_total counter",
        ]
        with self._lock:
            for (method, path, status_code), count in sorted(
                self._request_count.items()
            ):
                lines.append(
                    "sensorhub_http_requests_total"
                    f'{{method="{method}",path="{path}",status="{status_code}"}} '
                    f"{count}"
                )

            lines.extend(
                [
                    "# HELP sensorhub_http_request_duration_seconds "
                    "Tiempo acumulado de solicitudes HTTP.",
                    "# TYPE sensorhub_http_request_duration_seconds summary",
                ]
            )
            for (method, path), (count, total) in sorted(
                self._request_duration.items()
            ):
                labels = f'method="{method}",path="{path}"'
                lines.append(
                    "sensorhub_http_request_duration_seconds_count"
                    f"{{{labels}}} {count}"
                )
                lines.append(
                    "sensorhub_http_request_duration_seconds_sum"
                    f"{{{labels}}} {total:.9f}"
                )

        return "\n".join(lines) + "\n"


metrics = MetricsRegistry()
