FROM python:3.9-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY api_script.py .


RUN mkdir -p /data
ENV OUTPUT_DIR=/data


RUN chmod +x api_script.py


CMD ["python", "api_script.py"]
