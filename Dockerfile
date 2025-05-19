FROM python:3.12-slim
LABEL maintainer="andresluna2007@gmail.com"

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080


CMD ["python", "-m", "app.main"]
