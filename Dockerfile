FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    weasyprint \
    cron \
    fonts-dejavu-core \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile.lock Pipfile ./

RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py tailwind install
RUN python manage.py tailwind install

# Expose Django and Tailwind ports
EXPOSE 8000
EXPOSE 1912

CMD ["/bin/bash"]
