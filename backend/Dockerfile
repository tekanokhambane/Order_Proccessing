FROM python:3.11.4-alpine

WORKDIR /usr/src/app

# prevent python from writing .pyc files to the container
ENV PYTHONDONTWRITEBYTECODE 1

# prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apk update && apk add --no-cache \
    mariadb-dev \
    gcc \
    musl-dev \
    && rm -rf /var/cache/apk/*


RUN  pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
# change permissions of run_build.sh
# RUN chmod +x ./run_build.sh
RUN ls -la /usr/src/app
COPY . /usr/src/app/


