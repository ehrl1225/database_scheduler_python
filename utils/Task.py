from typing import Callable


class Task:
    """
    백그라운드로 실행할 함수들을 담습니다.
    :var pre_id: 과거의 pid
    """

    pre_id: int = 0

    def __init__(self, job: Callable, count: int, return_job:Callable = None):
        self.current_id = Task.pre_id + 1
        Task.pre_id = Task.pre_id + 1
        self.job = job
        self.count = count
        self.return_job = return_job

    def __call__(self, *args, **kwargs):
        if self.count > 0:
            self.job()
            self.count -= 1
        elif self.count == -1:
            self.job()
        if self.return_job is not None:
            self.return_job()

    def get_id(self):
        return self.current_id

    def can_run(self):
        if self.count > 0:
            return True
        elif self.count == -1:
            return True
        else:
            return False
