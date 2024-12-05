from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['broker_url'] = 'redis://redis:6379/0'
app.config['result_backend'] = 'redis://redis:6379/0'

celery = Celery('tasks', 
                broker_url='redis://redis:6379/0', 
                result_backend='redis://redis:6379/0')