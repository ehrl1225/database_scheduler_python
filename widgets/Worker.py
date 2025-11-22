from PyQt5.QtCore import QThread
from utils.Task import Task
import time


class Worker(QThread):
    task_list: list[Task] = []
    go: bool = True

    def __init__(self):
        super().__init__()

    @staticmethod
    def del_task(task: Task):
        if task in Worker.task_list:
            Worker.task_list.remove(task)

    def run(self) -> None:
        while Worker.go:
            for t_index, t in enumerate(Worker.task_list):
                if t.can_run():
                    t()
                else:
                    del Worker.task_list[t_index]
            time.sleep(0.1)
