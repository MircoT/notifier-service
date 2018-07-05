FROM python:3.7.0-alpine3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY notify_service.py .

ENV PORT=8080
EXPOSE 8080

ENTRYPOINT [ "python", "./notify_service.py" ]