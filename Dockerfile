FROM python:3.10.0-slim

# install needed packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN apt-get update -y
RUN apt-get install pkg-config -y
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn core.wsgi
