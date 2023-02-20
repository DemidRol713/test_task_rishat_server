FROM python:3.10-alpine
# set work directory
WORKDIR /usr/src/test_task_rishat
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip3 install --upgrade pip
RUN apk update \
    && apk add libpq-dev gcc

COPY requirements.txt .
RUN pip3 install -r ./requirements.txt

# copy project
COPY test_task_rishat_1 .

ENTRYPOINT ["/usr/src/test_task_rishat/entrypoint.sh"]