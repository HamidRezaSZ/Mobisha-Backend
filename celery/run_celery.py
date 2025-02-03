from celery.schedules import crontab
from tasks.price_update_service import celery_app

celery_app.conf.beat_schedule = {
    'update_prices_every_5_minutes': {
        'task': 'update_prices',
        'schedule': crontab(minute='*/5'),
    },
}

if __name__ == "__main__":
    celery_app.start()