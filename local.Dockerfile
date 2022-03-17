FROM python:3.10-alpine3.15
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .


RUN  apk update \
  && apk add --no-cache gcc musl-dev postgresql-dev python3-dev \
  && pip install --upgrade pip

RUN python -m pip install -r requirements.txt


COPY . .

CMD [ "sh", "entrypoint.sh" ]
