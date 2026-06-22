"""Represent a psychology trial as an object."""
from dataclasses import dataclass


@dataclass
class Trial:
    participant: str
    stimulus: str
    response: str
    reaction_time_ms: float

    def is_fast(self) -> bool:
        return self.reaction_time_ms < 500


trial = Trial("S001", "RED/blue", "j", 438.5)
print(trial)
print("快速反应：", trial.is_fast())
