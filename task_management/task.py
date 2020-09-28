from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Task:
    skill: str
    params: list
    worker_type: str
    task_id: int = None
    # birth_timestamp: str = field(default_factory=lambda: datetime.now().strftime("%m/%d/%Y, %H:%M:%S:%f"))

    def to_dict(self):
        return dict({'task_id': self.task_id,
                     'skill': self.skill,
                     'params': self.params,
                     'worker_type': self.worker_type})

    @staticmethod
    def to_task(task_as_dict):
        return Task(task_id=task_as_dict['task_id'], skill=task_as_dict['skill'],
                    params=task_as_dict['params'], worker_type=task_as_dict['worker_type'])
