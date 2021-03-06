from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Task:
    method: str
    params: list
    birth_timestamp: str = field(default_factory=lambda: datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f"))

    def to_dict(self):
        return dict({'method': self.method,
                     'params': self.params,
                     'birth_timestamp': self.birth_timestamp})

    @staticmethod
    def to_task(task_as_dict):
        return Task(task_as_dict['method'], task_as_dict['params'], task_as_dict['birth_timestamp'])
