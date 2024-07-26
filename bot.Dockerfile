FROM python:3.12.4-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot bot

COPY entrypoint.sh /usr/local/bin/

ENTRYPOINT ["entrypoint.sh"]
