"""
voice/metrics.py

Enterprise Metrics & Telemetry
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from threading import Lock
from typing import Dict


@dataclass(slots=True)
class TimerMetric:

    count: int = 0

    total_time: float = 0.0

    min_time: float = float("inf")

    max_time: float = 0.0

    @property
    def average(self):

        if self.count == 0:
            return 0.0

        return self.total_time / self.count

    def update(self, duration: float):

        self.count += 1

        self.total_time += duration

        self.min_time = min(

            self.min_time,

            duration,

        )

        self.max_time = max(

            self.max_time,

            duration,

        )


class MetricsCollector:
    """
    Enterprise Metrics Collector.

    Tracks:

    ✔ STT latency

    ✔ TTS latency

    ✔ AI latency

    ✔ Playback latency

    ✔ Recording latency

    ✔ Errors

    ✔ Wake Word count

    ✔ Speech count

    ✔ Sessions

    ✔ Requests
    """

    def __init__(self):

        self._lock = Lock()

        self._timers: Dict[str, TimerMetric] = {}

        self._counters: Dict[str, int] = {}

    # --------------------------------------------------

    def increment(

        self,

        name: str,

        value: int = 1,

    ):

        with self._lock:

            self._counters[name] = (

                self._counters.get(name, 0)

                + value

            )

    # --------------------------------------------------

    def timer(self, name: str):

        return TimerContext(

            self,

            name,

        )

    # --------------------------------------------------

    def record(

        self,

        name: str,

        duration: float,

    ):

        with self._lock:

            metric = self._timers.setdefault(

                name,

                TimerMetric(),

            )

            metric.update(

                duration,

            )

    # --------------------------------------------------

    def counter(

        self,

        name: str,

    ):

        return self._counters.get(

            name,

            0,

        )

    # --------------------------------------------------

    def timing(

        self,

        name: str,

    ):

        return self._timers.get(

            name,

            TimerMetric(),

        )

    # --------------------------------------------------

    def snapshot(self):

        with self._lock:

            return {

                "counters": self._counters.copy(),

                "timers": {

                    key: {

                        "count": value.count,

                        "average": value.average,

                        "min": value.min_time,

                        "max": value.max_time,

                        "total": value.total_time,

                    }

                    for key, value

                    in self._timers.items()

                },

            }


class TimerContext:

    def __init__(

        self,

        metrics: MetricsCollector,

        metric: str,

    ):

        self.metrics = metrics

        self.metric = metric

        self.start = 0.0

    def __enter__(self):

        self.start = time.perf_counter()

        return self

    def __exit__(

        self,

        exc_type,

        exc,

        tb,

    ):

        elapsed = (

            time.perf_counter()

            - self.start

        )

        self.metrics.record(

            self.metric,

            elapsed,

        )