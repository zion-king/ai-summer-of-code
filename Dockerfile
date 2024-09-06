FROM python:3.10

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# COPY requirements.txt /app/requirements.txt
COPY src/week_3/day_6_chat_engine/requirements.txt /app/requirements.txt

RUN pip3 install --cache-dir=/var/tmp/ torch==2.3.1 --index-url https://download.pytorch.org/whl/cpu && \
pip3 install --no-cache-dir -r requirements.txt && \
apt-get update -y --no-install-recommends

# COPY . /app
COPY src/week_3/day_6_chat_engine /app

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable for app to run in production mode
ENV APP_ENV=production

RUN ls -la /app/

# Use uvicorn workers with Gunicorn
ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker"]
CMD ["src/week_3/day_6_chat_engine/app:app", "--bind", "0.0.0.0:8001", "--timeout", "900", "--preload"]
