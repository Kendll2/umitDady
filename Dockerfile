FROM python:3.11-slim-bullseye
     
WORKDIR /app      
    
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Kendll2/umitDady.git .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["gunicorn", "--workers", "4", "--threads", "2", "--bind", "0.0.0.0:7860", "app:app"]
