from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Task:
    method: str
    params: list
    birth_timestamp: str = field(default_factory=lambda: datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f"))