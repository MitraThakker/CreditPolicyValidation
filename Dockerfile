FROM python:3.9-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["/bin/sh", "./run.sh"]
