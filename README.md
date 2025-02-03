# Digikala Backend

## How to Run
1. Start MongoDB:
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo
   ```

2. Start RabbitMQ:
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run Database Setup:
   ```bash
   python database_setup.py
   ```

5. Run Celery workers:
   ```bash
   celery -A tasks.price_update_service worker --loglevel=info
   celery -A tasks.insert_log worker --loglevel=info
   ```

6. Start Celery scheduler:
   ```bash
   celery -A celery.run_celery beat --loglevel=info
   ```

7. Run FastAPI services:
   ```bash
   uvicorn auth.auth_api:app --reload --port 8000
   uvicorn products.update_product:app --reload --port 8001
   ```
