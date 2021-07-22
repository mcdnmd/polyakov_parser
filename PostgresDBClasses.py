import psycopg2

from loguru import logger
from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase

db = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    # идентификатор задачи
    id = IntegerField(unique=True)
    # Ќомер задани€
    number = IntegerField()
    # формулировка задач
    text = TextField()
    # ответ на задачу
    answer = TextField()

    class Meta:
        table_name = 'tasks'


class DataBaseHandler:
    def __init__(self, dbname, user='postgres', password=None, host='127.0.0.1', port='5432'):
        if password is None:
            logger.error('DataBase password not passed')
            self.conn = None
        else:
            try:
                self.conn = PooledPostgresqlExtDatabase(dbname,
                                                        user=user,
                                                        password=password,
                                                        host=host,
                                                        port=port,
                                                        max_connections=8,
                                                        stale_timeout=300)
            except Exception as err:
                logger.exception(err)
                self.conn = None
            else:
                db.initialize(self.conn)
                logger.success('DB connected')
                self.create_models()
                logger.success('DB ready')

    def create_models(self) -> None:
        try:
            self.conn.create_tables([Task])
        except Exception as err:
            logger.exception(err)