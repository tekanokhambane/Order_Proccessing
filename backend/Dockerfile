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
COPY . /usr/src/app/
COPY ./run_build.sh /usr/src/app/

ENV PORT 8001


# export env from .evn file
# RUN export $(grep -v '^#' .env | xargs)
# EXPOSE 8001
# ENTRYPOINT ["sh", "./run_build.sh"]

CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--workers", "4", "--port", "8001"]


