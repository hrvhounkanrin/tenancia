from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y):
    """
     Mini  implementation test.
    :param x:
    :param y:
    :return:
    """
    return x + y
