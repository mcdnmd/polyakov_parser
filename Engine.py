import os

from PostgresDBClasses import *
from Task import TaskBasic
from TaskParser import TaskParser


class Engine:
    def __init__(self):
        self.db = None
        self._init_db()
        self.task_parser = TaskParser()

    def _init_db(self) -> None:
        dbname = os.getenv('db_name')
        user = os.getenv('user')
        password = os.getenv('passwd')
        host = os.getenv('host')
        self.db = DataBaseHandler(dbname=dbname, user=user, password=password, host=host)

    def start(self, start=1, end=10):
        for idx in range(start, end):
            task = self.task_parser.parse(idx)
            self.upload_task_in_db(task)

    @staticmethod
    def upload_task_in_db(task: TaskBasic):
        with db.atomic():
            id = (Task
                  .insert(id=task.id,
                          text=task.text,
                          answer=task.ans)
                  .execute())
            print(id)
