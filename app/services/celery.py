from celery import Celery
from dotenv import load_dotenv

load_dotenv() 

app = Celery(
    'proj',
    broker='amqp://user:password@localhost:5672//',
    backend='redis://localhost:6380/0', 
    include=['app.services.task']
)

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()