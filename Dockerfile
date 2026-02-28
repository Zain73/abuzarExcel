FROM python:3.12-slim

RUN apt-get update && apt-get install -y libreoffice && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY convert.py .

CMD ["python3", "convert.py"]
