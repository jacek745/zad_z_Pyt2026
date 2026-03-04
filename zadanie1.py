from dataclasses import dataclass
from datetime import datetime, date
from typing import Iterable, Iterator, Optional


@dataclass
class Activity:
    date: date
    athlete: str
    type: str
    distance_km: float
    time_min: float

    def __post_init__(self) -> None:
        if not self.athlete.strip():
            raise ValueError("Athlete nie może być pusty.")

        if self.distance_km <= 0:
            raise ValueError("distance_km musi być > 0.")

        if self.time_min <= 0:
            raise ValueError("time_min musi być > 0.")

        self.type = self.type.strip().lower()

    @property
    def pace_min_per_km(self) -> Optional[float]:
        if self.type != "run":
            return None
        return self.time_min / self.distance_km

    @property
    def speed_km_per_h(self) -> float:
        return self.distance_km / (self.time_min / 60)

    @property
    def is_long(self) -> bool:
        return self.distance_km >= 20


def source_lines(text: str) -> Iterator[str]:
    for line in text.splitlines():
        yield line


def parse(lines: Iterable[str]) -> Iterator[Activity]:
    for line in lines:
        try:
            parts = line.split("|")
            if len(parts) != 5:
                continue

            d = datetime.strptime(parts[0], "%Y-%m-%d").date()
            athlete = parts[1]
            typ = parts[2]
            dist = float(parts[3])
            time = float(parts[4])

            yield Activity(d, athlete, typ, dist, time)

        except Exception:
            continue


def only_type(activities: Iterable[Activity], wanted_type: str) -> Iterator[Activity]:
    wanted_type = wanted_type.lower()
    for a in activities:
        if a.type == wanted_type:
            yield a


def only_athlete(activities: Iterable[Activity], athlete: str) -> Iterator[Activity]:
    athlete = athlete.lower()
    for a in activities:
        if a.athlete.lower() == athlete:
            yield a


class TrainingLog:
    def __init__(self, activities: Iterable[Activity]):
        self.activities = list(activities)

    def total_distance(self, type: Optional[str] = None) -> float:
        if type:
            type = type.lower()
            return sum(a.distance_km for a in self.activities if a.type == type)
        return sum(a.distance_km for a in self.activities)

    def total_time(self, type: Optional[str] = None) -> float:
        if type:
            type = type.lower()
            return sum(a.time_min for a in self.activities if a.type == type)
        return sum(a.time_min for a in self.activities)

    def best_pace(self) -> Optional[float]:
        runs = [a for a in self.activities if a.type == "run"]
        if not runs:
            return None
        return min(a.pace_min_per_km for a in runs)

    def long_runs(self) -> list[Activity]:
        return [a for a in self.activities if a.type == "run" and a.is_long]

    @property
    def summary(self) -> str:
        total_dist = self.total_distance()
        total_time = self.total_time()
        best = self.best_pace()

        lines = [
            f"Łączny dystans: {total_dist:.1f} km",
            f"Łączny czas: {total_time:.1f} min",
            f"Najlepsze tempo (run): {best:.2f} min/km" if best else "Brak biegów",
            f"Liczba długich biegów: {len(self.long_runs())}",
        ]
        return "\n".join(lines)


raw = """2026-03-01|Marcin|run|12.5|65
2026-03-02|Marcin|run|8.0|44
2026-03-02|Ewa|bike|30.0|75
2026-03-03|Marcin|run|21.1|110
BAD|LINE
2026-03-03|Ewa|run|5.0|33"""

lines = source_lines(raw)
activities = list(parse(lines))

log = TrainingLog(activities)

print(log.summary)
print("Długie biegi:", log.long_runs())
print("Dystans biegowy Marcina:", log.total_distance("run"))
