FROM python:3.9-slim-bullseye

ENV PORT 8080
EXPOSE $PORT
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY download_model.py /app/download_model.py
RUN python download_model.py
COPY . /app/

CMD uvicorn server:app --host 0.0.0.0 --port $PORT

