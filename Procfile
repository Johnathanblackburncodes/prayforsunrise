
web: uvicorn prayforsunrise.asgi:application --host=0.0.0.0 --port=${PORT:-5000}
worker: ptyhon manage.py runworker channel_layer -v2
