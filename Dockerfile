FROM python:3.12-slim

WORKDIR /app

COPY zscaler-chain.pem /usr/local/share/ca-certificates/zscaler-chain.crt

RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]