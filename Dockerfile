FROM python:3.9-slim AS backend-builder

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN chmod +x init.sh
CMD ["./init.sh"]
