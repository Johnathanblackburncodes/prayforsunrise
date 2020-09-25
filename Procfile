
web: uvicorn prayforsunrise.asgi:application --host=0.0.0.0 --port=${PORT:-5000}
worker: python3 manage.py runworker channel_layer -v2
