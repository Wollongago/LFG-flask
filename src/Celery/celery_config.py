"""
Settings for Celery worker and beat services.

"""

import config
from kombu import Queue

# broker_url = 'amqp://KycKyc:%s@%s//' % (config.Global.BROKER_PASSWORD, config.Global.BROKER_ADDRESS)
broker_url = config.Global.BROKER_URL
broker_pool_limit = 16  # 16 connection, default 10.

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
# accept_content = ['application/json', 'application/x-python-serialize']
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'
worker_pool_restarts = True
worker_hijack_root_logger = False

# Define queues
task_default_queue = 'celery_default'
task_queues = (
    Queue('celery_default', routing_key='task.#'),
    Queue('celery_statistics', routing_key='statistics.#'),
    Queue('celery_notifications', routing_key='notifications.#'),
)
task_routes = {
    'statistics.*': {
        'queue': 'celery_statistics',
        'routing_key': 'statistics.default',
    },
    'verifying.*': {
        'queue': 'celery_default',
        'routing_key': 'task.verifying',
    },
    'notifications.*': {
        'queue': 'celery_notifications',
        'routing_key': 'notifications.default',
    }
}
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'

task_acks_late = True  # ack after all calculations
worker_prefetch_multiplier = 1  # 1 message per 1 worker

# task_time_limit = 60*60  # seconds, then terminate
# task_soft_time_limit = 30*60  # seconds, then throw soft limit exception

timezone = 'UTC'

# Result Backend: MongoDB
# result_backend = 'mongodb://%s:%s/' % ("mongodb", 27017)
# mongodb_backend_settings = {
#     'database': 'Warframe',
#     'taskmeta_collection': 'celery_task_results',
# }

# result Backend: Reddis
result_backend = f"redis://:{config.credentials.CACHE_REDIS_PASSWORD}@redis:6379/3"
result_backend_transport_options = {
    'retry_policy': {
        'timeout': 5.0
    }
}
result_expires = 60*60*24  # Once in a day.

# Scheduler Settings in case of DB usage.
CELERY_MONGODB_SCHEDULER_DB = "LFG"
CELERY_MONGODB_SCHEDULER_COLLECTION = "celery_schedules"
CELERY_MONGODB_SCHEDULER_URL = 'mongodb://%s:%s/' % ("mongodb", 27017)

# print broker_url
print(f"broker_url: {broker_url}")